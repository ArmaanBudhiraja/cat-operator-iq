import React, { useState } from 'react';
import { api } from '../services/api';
import { useRole } from '../context/RoleContext';
import { Button } from '../components/ui/Button';
import { Send, ArrowRight, Info, RefreshCw } from 'lucide-react';

interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  evidence?: string[];
  nextStep?: string;
  disclaimer?: string;
  citations?: string[];
}

export const AssistantPage: React.FC = () => {
  const { activeOperatorId, activeMachineId } = useRole();

  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);

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
      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: res.answer,
        evidence: res.evidence,
        nextStep: res.recommended_next_step,
        disclaimer: res.safety_disclaimer,
        citations: res.citations,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: 'The telemetry intelligence service is momentarily unavailable. Please retry.',
        disclaimer: 'AI-generated recommendations are advisory and must not replace official procedures.',
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12 max-w-4xl mx-auto font-sans">
      {/* Header */}
      <div className="flex flex-wrap items-baseline justify-between gap-4 pb-3 border-b border-[#E5E5E5]">
        <div>
          <h1 className="text-2xl font-semibold text-[#171717] tracking-tight">
            OperatorIQ Assistant
          </h1>
          <p className="text-xs text-[#737373] mt-0.5">
            Operational intelligence · Ask about your machine, tasks, safety or performance.
          </p>
        </div>

        {messages.length > 0 && (
          <button
            onClick={() => setMessages([])}
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
                <div className="text-base font-semibold text-[#171717]">
                  OperatorIQ
                </div>
                <p className="text-xs text-[#737373]">
                  Operational intelligence assistant
                </p>
              </div>

              <p className="text-xs text-[#525252] max-w-md mx-auto leading-relaxed">
                Ask about machine condition, task predictions, safety guidelines or historical baseline deviations.
              </p>

              <div className="space-y-2 pt-2">
                <div className="text-xs text-[#737373] mb-2 font-medium">
                  Suggested questions:
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
                  <div className="text-xs text-[#737373] font-medium">
                    {m.sender === 'user' ? `Operator (${activeOperatorId})` : 'OperatorIQ Assistant'}
                  </div>

                  {m.sender === 'user' ? (
                    <div className="p-3.5 bg-[#F5F5F5] border border-[#E5E5E5] rounded-[6px] text-[#171717] leading-relaxed">
                      {m.text}
                    </div>
                  ) : (
                    <div className="p-5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] space-y-4 shadow-xs">
                      {/* 1. Answer */}
                      <div className="text-sm text-[#171717] leading-relaxed">
                        {m.text}
                      </div>

                      {/* 2. Evidence */}
                      {m.evidence && m.evidence.length > 0 && (
                        <div className="space-y-1.5 pt-2 border-t border-[#E5E5E5]">
                          <div className="text-xs font-semibold text-[#171717]">
                            Evidence
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
                <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] text-[#737373] text-xs shadow-xs">
                  Synthesizing telemetry stream and Caterpillar procedural guidelines...
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
