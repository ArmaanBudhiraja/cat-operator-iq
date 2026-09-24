import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useRole } from '../context/RoleContext';
import { Button } from '../components/ui/Button';
import { Send, ArrowRight, Info, RefreshCw, Sparkles, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { AssistantStatus } from '../types';

interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  evidence?: string[];
  nextStep?: string;
  disclaimer?: string;
  citations?: string[];
  is_fallback?: boolean;
  ai_provider?: string;
  fallback_reason?: string | null;
}

export const AssistantPage: React.FC = () => {
  const { activeOperatorId, activeMachineId } = useRole();

  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [status, setStatus] = useState<AssistantStatus | null>(null);
  const [lastFallback, setLastFallback] = useState<boolean | null>(null);

  // Load assistant configuration and readiness status
  useEffect(() => {
    let isMounted = true;
    api.getAssistantStatus()
      .then((data) => {
        if (isMounted) setStatus(data);
      })
      .catch((err) => {
        console.warn('Failed to load assistant status:', err);
      });
    return () => { isMounted = false; };
  }, []);

  const suggestedQuestions = [
    `Why is ${activeMachineId} showing a warning?`,
    'What should I focus on today?',
    'How long will my current task take?',
    'What changed in my machine\'s behavior?',
    'What training should I complete?',
  ];

  const handleSend = async (textToSend?: string) => {
    const text = (textToSend || query).trim();
    if (!text || loading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text,
    };

    setMessages((prev) => [...prev, userMsg]);
    setQuery('');
    setLoading(true);

    try {
      const res = await api.queryAssistant(text, activeOperatorId, activeMachineId);
      const isFallback = Boolean(res.is_fallback);
      setLastFallback(isFallback);

      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: res.answer,
        evidence: res.evidence,
        nextStep: res.recommended_next_step,
        disclaimer: res.safety_disclaimer,
        citations: res.citations,
        is_fallback: isFallback,
        ai_provider: res.ai_provider,
        fallback_reason: res.fallback_reason,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setLastFallback(true);
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: 'The telemetry intelligence service is momentarily unavailable. Live AI service could not be reached, and response was synthesized via local fallback procedures.',
        disclaimer: 'AI-generated recommendations are advisory and must not replace official procedures.',
        is_fallback: true,
        ai_provider: 'Local Rule-Based Assistant (Offline Fallback)',
        fallback_reason: err?.message || 'Network connection to AI endpoint failed. Operating in local safety rule mode.',
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12 max-w-4xl mx-auto font-sans">
      {/* Header with Live AI Status Signal */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-[#E5E5E5]">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-semibold text-[#171717] tracking-tight">
              OperatorIQ Assistant
            </h1>

            {/* AI Status Badge Signal */}
            {lastFallback === true ? (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-900 border border-amber-300">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-600 animate-pulse" />
                <span>Live AI Offline · Fallback Mode Active</span>
              </span>
            ) : lastFallback === false ? (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-800 border border-emerald-300">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span>Live AI Online ({messages[messages.length - 1]?.ai_provider || status?.provider || 'Gemini'})</span>
              </span>
            ) : status?.ai_configured ? (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-800 border border-emerald-300">
                <span className="relative flex h-2 w-2">
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span>Live AI Ready ({status.provider})</span>
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-neutral-100 text-neutral-700 border border-neutral-300">
                <span className="w-2 h-2 rounded-full bg-neutral-400"></span>
                <span>Local Rule Mode (Offline)</span>
              </span>
            )}
          </div>

          <p className="text-xs text-[#737373] mt-1">
            Operational intelligence · In-cab telemetry analysis, task projections, and Caterpillar safety procedures.
          </p>
        </div>

        {messages.length > 0 && (
          <button
            onClick={() => {
              setMessages([]);
              setLastFallback(null);
            }}
            className="text-xs text-[#737373] hover:text-[#171717] flex items-center gap-1.5 transition-colors font-medium"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Reset conversation</span>
          </button>
        )}
      </div>

      {/* Main Interface */}
      <div className="min-h-[500px] flex flex-col justify-between space-y-6">
        {/* Messages or Empty State */}
        <div className="flex-1 space-y-6">
          {messages.length === 0 ? (
            /* Empty State */
            <div className="py-12 text-center space-y-5">
              <div className="space-y-1">
                <div className="text-base font-semibold text-[#171717] flex items-center justify-center gap-2">
                  <Sparkles className="w-4 h-4 text-amber-500" />
                  <span>OperatorIQ In-Cab Intelligence</span>
                </div>
                <p className="text-xs text-[#737373]">
                  Connected to machine {activeMachineId} live telemetry stream
                </p>
              </div>

              <p className="text-xs text-[#525252] max-w-md mx-auto leading-relaxed">
                Ask about machine health, active safety alerts, task completion predictions, or recommended procedures.
                When Live AI is connected, queries are answered using Gemini models. If the online AI is unavailable or rate-limited, the system automatically rolls back to onboard telemetry rules.
              </p>

              <div className="space-y-2 pt-2">
                <div className="text-xs text-[#737373] mb-2 font-medium">
                  Suggested inquiries:
                </div>
                <div className="flex flex-wrap justify-center gap-2 max-w-xl mx-auto">
                  {suggestedQuestions.map((q, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSend(q)}
                      className="px-3 py-1.5 rounded-[4px] border border-[#E5E5E5] bg-[#FFFFFF] hover:border-[#737373] hover:bg-[#FAFAFA] text-xs text-[#171717] transition-colors shadow-xs"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            /* Conversation Stream */
            <div className="space-y-6 text-xs">
              {messages.map((m) => (
                <div key={m.id} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs text-[#737373] font-medium px-0.5">
                    <span>
                      {m.sender === 'user' ? `Operator (${activeOperatorId})` : 'OperatorIQ Assistant'}
                    </span>

                    {/* Per-Message AI vs Fallback Indicator */}
                    {m.sender === 'assistant' && (
                      <div>
                        {m.is_fallback ? (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-amber-50 text-amber-900 border border-amber-300">
                            <AlertTriangle className="w-3 h-3 text-amber-600" />
                            <span>Fallback Mode (Local Rules)</span>
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-medium bg-emerald-50 text-emerald-800 border border-emerald-200">
                            <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                            <span>{m.ai_provider || 'Live AI'}</span>
                          </span>
                        )}
                      </div>
                    )}
                  </div>

                  {m.sender === 'user' ? (
                    <div className="p-3.5 bg-[#F5F5F5] border border-[#E5E5E5] rounded-[6px] text-[#171717] leading-relaxed">
                      {m.text}
                    </div>
                  ) : (
                    <div className="p-5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] space-y-4 shadow-xs">
                      {/* Signal Banner if Fallback Mode was triggered */}
                      {m.is_fallback && (
                        <div className="p-3 bg-amber-50/80 border border-amber-200 rounded-[6px] text-xs text-amber-900 flex items-start gap-2.5">
                          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                          <div className="space-y-0.5">
                            <div className="font-semibold text-amber-950">
                              Live AI Offline Signal
                            </div>
                            <p className="text-xs text-amber-900 leading-relaxed">
                              {m.fallback_reason || 'Live AI was unreachable or rate-limited. This response was automatically synthesized by the onboard deterministic Caterpillar rule engine.'}
                            </p>
                          </div>
                        </div>
                      )}

                      {/* 1. Answer */}
                      <div className="text-sm text-[#171717] leading-relaxed">
                        {m.text}
                      </div>

                      {/* 2. Evidence */}
                      {m.evidence && m.evidence.length > 0 && (
                        <div className="space-y-1.5 pt-2 border-t border-[#E5E5E5]">
                          <div className="text-xs font-semibold text-[#171717]">
                            Evidence & Telemetry Corroboration
                          </div>
                          <div className="space-y-1 text-xs text-[#525252]">
                            {m.evidence.map((ev, idx) => (
                              <div key={idx} className="flex items-start gap-1.5">
                                <span className="text-[#737373]">•</span>
                                <span>{ev}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* 3. Recommended Next Step */}
                      {m.nextStep && (
                        <div className="space-y-1.5 pt-2 border-t border-[#E5E5E5]">
                          <div className="text-xs font-semibold text-[#171717] flex items-center gap-1.5">
                            <ArrowRight className="w-3.5 h-3.5 text-[#171717]" />
                            <span>Recommended next step</span>
                          </div>
                          <p className="text-xs text-[#525252] leading-relaxed">
                            {m.nextStep}
                          </p>
                        </div>
                      )}

                      {/* Citations */}
                      {m.citations && m.citations.length > 0 && (
                        <div className="text-xs text-[#737373] pt-2 border-t border-[#E5E5E5]">
                          Reference manuals: {m.citations.join(' · ')}
                        </div>
                      )}

                      {/* Safety Disclaimer */}
                      {m.disclaimer && (
                        <div className="pt-2 border-t border-[#E5E5E5] text-xs text-[#737373] flex items-center gap-1.5">
                          <Info className="w-3.5 h-3.5 text-[#737373] shrink-0" />
                          <span>{m.disclaimer}</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}

              {loading && (
                <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] text-[#737373] text-xs shadow-xs flex items-center gap-2">
                  <div className="w-3 h-3 border-2 border-neutral-400 border-t-transparent rounded-full animate-spin"></div>
                  <span>Synthesizing live telemetry and querying operational intelligence...</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="pt-3 border-t border-[#E5E5E5]">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2.5"
          >
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about machine telemetry, tasks, or safety guidelines..."
              className="flex-1 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] p-2.5 text-xs text-[#171717] placeholder-[#737373] focus:border-[#737373] focus:outline-none shadow-xs font-sans"
              disabled={loading}
            />

            <Button
              type="submit"
              variant="primary"
              size="md"
              disabled={!query.trim() || loading}
              icon={<Send className="w-3.5 h-3.5 text-current" />}
            >
              Ask
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};
