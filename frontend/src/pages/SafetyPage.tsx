import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useSimulation } from '../context/SimulationContext';
import { useRole } from '../context/RoleContext';
import { ProximityRadar } from '../components/ProximityRadar';
import { SimulationControls } from '../components/SimulationControls';
import { SkeletonCard } from '../components/StateViews';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { SectionHeader } from '../components/ui/SectionHeader';
import { Info } from 'lucide-react';

export const SafetyPage: React.FC = () => {
  const { liveState } = useSimulation();
  const { activeMachineId } = useRole();
  const [safetyEvents, setSafetyEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadEvents = async () => {
    try {
      setLoading(true);
      const data = await api.getSafetyEvents(activeMachineId);
      setSafetyEvents(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, [activeMachineId]);

  const score = liveState?.safety_score !== undefined ? liveState.safety_score : 18.0;
  const safetyScoreValue = Math.max(0, 100 - score);
  const statusLabel = liveState?.status_label || (score > 60 ? 'Critical' : score > 35 ? 'High risk' : score > 20 ? 'Attention' : 'Normal');
  const riskLevel = liveState?.risk_level || 'LOW';
  const activeAlerts = liveState?.active_alerts || [];
  const radarWorkers = liveState?.radar_objects || [];
  const breakdown = liveState?.factor_breakdown || {
    seatbelt_risk: 0,
    proximity_risk: 0,
    fatigue_risk: 0,
    temperature_risk: 0,
    vibration_risk: 0,
    behavior_risk: 0,
    environmental_risk: 0,
  };

  const isCritical = riskLevel === 'CRITICAL' || score > 60;
  const isHigh = riskLevel === 'HIGH' || score > 35;
  const isWarning = riskLevel === 'MEDIUM' || score > 20;

  const statusVariant = isCritical ? 'critical' : isHigh ? 'high' : isWarning ? 'warning' : 'safe';

  return (
    <div className="space-y-6 pb-12 max-w-6xl mx-auto font-sans">
      {/* Header */}
      <div className="flex flex-wrap items-baseline justify-between gap-4 pb-3 border-b border-[#E5E5E5]">
        <div>
          <h1 className="text-2xl font-semibold text-[#171717] tracking-tight">
            Safety Center
          </h1>
          <p className="text-xs text-[#737373] mt-0.5">
            Current machine · {activeMachineId}
          </p>
        </div>

        <Badge variant={statusVariant} size="md">
          {statusLabel}
        </Badge>
      </div>

      {/* Simulation Controls */}
      <SimulationControls />

      {/* Safety Status Hero */}
      <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-5 shadow-xs">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 divide-y md:divide-y-0 md:divide-x divide-[#E5E5E5]">
          <div className="md:pr-4">
            <div className="text-xs text-[#525252]">
              Safety status
            </div>
            <div className="text-3xl font-semibold text-[#171717] mt-1 tracking-tight">
              {statusLabel}
            </div>
            <p className="text-xs text-[#737373] mt-1">
              Continuous evaluation across 8 mechanical and proximity rules.
            </p>
          </div>

          <div className="pt-4 md:pt-0 md:px-4">
            <div className="text-xs text-[#525252]">
              Safety score
            </div>
            <div className="text-4xl font-semibold text-[#171717] mt-1 tabular-nums tracking-tight">
              {safetyScoreValue.toFixed(0)} <span className="text-sm text-[#737373] font-normal">/ 100</span>
            </div>
            <p className="text-xs text-[#737373] mt-1">
              Aggregated telemetry risk: {score.toFixed(1)} pts.
            </p>
          </div>

          <div className="pt-4 md:pt-0 md:pl-4">
            <div className="text-xs text-[#525252]">
              Perimeter exclusion
            </div>
            <div className="text-3xl font-semibold text-[#171717] mt-1 tabular-nums tracking-tight">
              {radarWorkers.filter((w) => w.distance <= 3.0).length} <span className="text-xs font-normal text-[#737373]">critical breaches</span>
            </div>
            <p className="text-xs text-[#737373] mt-1">
              {radarWorkers.length} personnel monitored in LiDAR zone.
            </p>
          </div>
        </div>
      </div>

      {/* Active Events & Timeline */}
      <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-5 shadow-xs space-y-4">
        <SectionHeader
          title="Active events & timeline"
          count={activeAlerts.length}
          description="Operational timeline of recent perimeter alerts and telemetry violations"
        />

        {activeAlerts.length > 0 && (
          <div className="space-y-2.5 mb-4">
            {activeAlerts.map((alert, idx) => (
              <div
                key={idx}
                className="p-4 bg-[#FFFFFF] border-2 border-[#111111] rounded-[6px] flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xs"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <Badge variant="critical">
                      {alert.severity}
                    </Badge>
                    <span className="text-xs font-semibold text-[#171717]">
                      {alert.title}
                    </span>
                  </div>
                  <p className="text-xs text-[#525252] mt-1">
                    {alert.message}
                  </p>
                  <div className="text-xs text-[#737373] mt-0.5">
                    Machine: {activeMachineId} · Rule: {alert.rule_id || 'PROX_INCURSION'} · Active
                  </div>
                </div>

                <div className="shrink-0">
                  <Button variant="primary" size="sm">
                    Review event
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Clean Timeline */}
        <div className="relative pl-6 space-y-4 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-[1px] before:bg-[#E5E5E5] text-xs">
          {loading ? (
            <SkeletonCard rows={3} />
          ) : safetyEvents.length === 0 ? (
            <div className="text-[#737373] text-xs py-2">
              08:00:00 · Normal operation resumed. All telemetry nominal.
            </div>
          ) : (
            safetyEvents.map((ev, idx) => (
              <div key={idx} className="relative">
                {/* Timeline Node Dot */}
                <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-[#FFFFFF] border-2 border-[#111111]" />

                <div className="flex flex-wrap items-baseline justify-between gap-2">
                  <div className="space-y-0.5">
                    <span className="text-[#171717] font-semibold text-xs">
                      {ev.event_type}
                    </span>
                    <p className="text-xs text-[#737373]">
                      {ev.details}
                    </p>
                  </div>

                  <div className="text-right text-xs text-[#737373] tabular-nums">
                    <span>{ev.timestamp?.split('T')[1]?.slice(0, 8) || '09:42:12'}</span>
                    <span className="ml-2 text-[#171717] font-mono font-medium">+{ev.risk_score} pts</span>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Proximity Radar */}
      <ProximityRadar workers={radarWorkers} machineId={activeMachineId} />

      {/* 8-Rule Scoring Model Matrix */}
      <div>
        <SectionHeader
          title="8-Rule scoring model matrix"
          description="Transparent additive scoring model components normalized across telemetry and perimeter inputs"
        />

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
            <div className="flex items-center justify-between text-[#737373] mb-1">
              <span className="font-mono text-xs">R1: SEATBELT</span>
              <span className={breakdown.seatbelt_risk ? 'text-[#171717] font-bold' : 'text-[#737373]'}>
                +{breakdown.seatbelt_risk || 0} pts
              </span>
            </div>
            <div className="text-xs font-semibold text-[#171717]">Restraint interlock</div>
            <div className="text-xs text-[#737373] mt-0.5">
              Unfastened during travel adds +35 pts.
            </div>
          </div>

          <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
            <div className="flex items-center justify-between text-[#737373] mb-1">
              <span className="font-mono text-xs">R2: PROXIMITY</span>
              <span className={breakdown.proximity_risk ? 'text-[#171717] font-bold' : 'text-[#737373]'}>
                +{breakdown.proximity_risk || 0} pts
              </span>
            </div>
            <div className="text-xs font-semibold text-[#171717]">LiDAR perimeter breach</div>
            <div className="text-xs text-[#737373] mt-0.5">
              &lt;3m adds +45 pts; 3–6m adds +25 pts.
            </div>
          </div>

          <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
            <div className="flex items-center justify-between text-[#737373] mb-1">
              <span className="font-mono text-xs">R3: FATIGUE</span>
              <span className={breakdown.fatigue_risk ? 'text-[#171717] font-bold' : 'text-[#737373]'}>
                +{breakdown.fatigue_risk || 0} pts
              </span>
            </div>
            <div className="text-xs font-semibold text-[#171717]">Alertness index</div>
            <div className="text-xs text-[#737373] mt-0.5">
              Fatigue index &gt; 0.75 adds +30 pts.
            </div>
          </div>

          <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
            <div className="flex items-center justify-between text-[#737373] mb-1">
              <span className="font-mono text-xs">R4: IDLE DURATION</span>
              <span className={breakdown.behavior_risk ? 'text-[#171717] font-bold' : 'text-[#737373]'}>
                +{breakdown.behavior_risk || 0} pts
              </span>
            </div>
            <div className="text-xs font-semibold text-[#171717]">Excess continuous idle</div>
            <div className="text-xs text-[#737373] mt-0.5">
              Idling &gt; 45 min adds +20 pts.
            </div>
          </div>

          <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
            <div className="flex items-center justify-between text-[#737373] mb-1">
              <span className="font-mono text-xs">R5: ENGINE TEMP</span>
              <span className={breakdown.temperature_risk ? 'text-[#171717] font-bold' : 'text-[#737373]'}>
                +{breakdown.temperature_risk || 0} pts
              </span>
            </div>
            <div className="text-xs font-semibold text-[#171717]">Thermal corridor limit</div>
            <div className="text-xs text-[#737373] mt-0.5">
              Coolant &gt; 105°C adds +35 pts.
            </div>
          </div>

          <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
            <div className="flex items-center justify-between text-[#737373] mb-1">
              <span className="font-mono text-xs">R6: VIBRATION</span>
              <span className={breakdown.vibration_risk ? 'text-[#171717] font-bold' : 'text-[#737373]'}>
                +{breakdown.vibration_risk || 0} pts
              </span>
            </div>
            <div className="text-xs font-semibold text-[#171717]">Undercarriage vibration</div>
            <div className="text-xs text-[#737373] mt-0.5">
              Vibration &gt; 3.8 mm/s adds +30 pts.
            </div>
          </div>

          <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
            <div className="flex items-center justify-between text-[#737373] mb-1">
              <span className="font-mono text-xs">R7: RECURRENCE</span>
              <span className="text-[#737373] font-bold">+0 pts</span>
            </div>
            <div className="text-xs font-semibold text-[#171717]">Event recurrence</div>
            <div className="text-xs text-[#737373] mt-0.5">
              3+ incidents within short window adds +25 pts.
            </div>
          </div>

          <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
            <div className="flex items-center justify-between text-[#737373] mb-1">
              <span className="font-mono text-xs">R8: COMBINATION</span>
              <span className={breakdown.environmental_risk ? 'text-[#171717] font-bold' : 'text-[#737373]'}>
                +{breakdown.environmental_risk || 0} pts
              </span>
            </div>
            <div className="text-xs font-semibold text-[#171717]">Adverse weather + load</div>
            <div className="text-xs text-[#737373] mt-0.5">
              Rain/storm + payload &gt; 18t adds +20 pts.
            </div>
          </div>
        </div>
      </div>

      {/* Advisory Disclaimer */}
      <div className="pt-3 border-t border-[#E5E5E5] flex items-center gap-2 text-xs text-[#737373]">
        <Info className="w-3.5 h-3.5 shrink-0 text-[#737373]" />
        <span>
          AI-generated recommendations are advisory and must not replace official operating procedures, safety procedures, operator training, or professional judgment.
        </span>
      </div>
    </div>
  );
};
