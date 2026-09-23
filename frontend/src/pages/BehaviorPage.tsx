import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useRole } from '../context/RoleContext';
import { AnomalyItem } from '../types';
import { SkeletonCard, ErrorState } from '../components/StateViews';
import { Badge } from '../components/ui/Badge';
import { SectionHeader } from '../components/ui/SectionHeader';

export const BehaviorPage: React.FC = () => {
  const { activeOperatorId } = useRole();
  const [anomalies, setAnomalies] = useState<AnomalyItem[]>([]);
  const [operatorDetail, setOperatorDetail] = useState<any | null>(null);
  const [modelMetrics, setModelMetrics] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [anomData, opData, metricsData] = await Promise.all([
        api.getAnomalies(),
        api.getOperatorDetail(activeOperatorId),
        api.getModelMetrics()
      ]);
      setAnomalies(anomData);
      setOperatorDetail(opData);
      setModelMetrics(metricsData);
    } catch (err: any) {
      setError(err.message || 'Failed to load behavior analytics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [activeOperatorId]);

  if (loading) {
    return <SkeletonCard rows={6} />;
  }

  if (error) {
    return <ErrorState error={error} onRetry={loadData} />;
  }

  const op = operatorDetail?.operator;
  const baselines = operatorDetail?.fleet_baselines;

  return (
    <div className="space-y-6 pb-12 max-w-6xl mx-auto font-sans">
      {/* Header */}
      <div className="flex flex-wrap items-baseline justify-between gap-4 pb-3 border-b border-[#E5E5E5]">
        <div>
          <h1 className="text-2xl font-semibold text-[#171717] tracking-tight">
            Behavior analytics
          </h1>
          <p className="text-xs text-[#737373] mt-0.5">
            Baseline deviations · Operator {activeOperatorId}
          </p>
        </div>

        <Badge variant="warning" size="sm">
          Isolation Forest active
        </Badge>
      </div>

      {/* Model Spec Bar */}
      <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] px-4 py-2.5 text-xs text-[#525252] shadow-xs flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <span className="text-[#171717] font-semibold">Model: Isolation Forest</span>
          <span className="text-[#D4D4D4]">·</span>
          <span>Contamination: 5.0%</span>
          <span className="text-[#D4D4D4]">·</span>
          <span>6 CAN-bus telemetry dimensions</span>
        </div>
        <div>
          Task regression R²: <span className="text-[#171717] font-semibold tabular-nums">{modelMetrics?.task_completion_model?.R2_score || 0.964}</span>
        </div>
      </div>

      {/* Baseline Deviations Section */}
      <div className="space-y-3">
        <SectionHeader
          title="Baseline comparisons"
          description="Deviations from operator and machine historical baselines"
        />

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          {/* Card 1: Idle Time */}
          <div className="p-4 bg-[#FFFFFF] border border-[#737373] rounded-[6px] flex flex-col justify-between space-y-3 shadow-xs">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-[#171717]">Idle time</span>
                <Badge variant="warning" size="sm">Unusual activity</Badge>
              </div>

              <div className="grid grid-cols-3 gap-2 my-2.5 py-2.5 border-y border-[#E5E5E5]">
                <div>
                  <span className="text-xs text-[#737373] block">Today</span>
                  <span className="text-sm font-semibold text-[#171717] tabular-nums">55 min</span>
                </div>
                <div>
                  <span className="text-xs text-[#737373] block">Baseline</span>
                  <span className="text-sm text-[#737373] tabular-nums">27 min</span>
                </div>
                <div>
                  <span className="text-xs text-[#737373] block">Diff</span>
                  <span className="text-sm font-semibold text-[#171717] tabular-nums">+28 min</span>
                </div>
              </div>
            </div>

            <p className="text-xs text-[#525252] leading-relaxed">
              Idle duration is significantly above historical baseline.
            </p>
          </div>

          {/* Card 2: Cycle Time */}
          <div className="p-4 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] flex flex-col justify-between space-y-3 shadow-xs">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-[#171717]">Cycle duration</span>
                <Badge variant="safe" size="sm">Nominal</Badge>
              </div>

              <div className="grid grid-cols-3 gap-2 my-2.5 py-2.5 border-y border-[#E5E5E5]">
                <div>
                  <span className="text-xs text-[#737373] block">Today</span>
                  <span className="text-sm font-semibold text-[#171717] tabular-nums">{op?.average_task_time || 54}m</span>
                </div>
                <div>
                  <span className="text-xs text-[#737373] block">Baseline</span>
                  <span className="text-sm text-[#737373] tabular-nums">{baselines?.fleet_avg_task_time || 60}m</span>
                </div>
                <div>
                  <span className="text-xs text-[#737373] block">Diff</span>
                  <span className="text-sm font-semibold text-[#171717] tabular-nums">-6 min</span>
                </div>
              </div>
            </div>

            <p className="text-xs text-[#525252] leading-relaxed">
              Cycle completion rate is 10% faster than fleet baseline.
            </p>
          </div>

          {/* Card 3: Vibration Amplitude */}
          <div className="p-4 bg-[#FFFFFF] border border-[#737373] rounded-[6px] flex flex-col justify-between space-y-3 shadow-xs">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-[#171717]">Vibration</span>
                <Badge variant="warning" size="sm">Elevated</Badge>
              </div>

              <div className="grid grid-cols-3 gap-2 my-2.5 py-2.5 border-y border-[#E5E5E5]">
                <div>
                  <span className="text-xs text-[#737373] block">Current</span>
                  <span className="text-sm font-semibold text-[#171717] tabular-nums">7.8</span>
                </div>
                <div>
                  <span className="text-xs text-[#737373] block">Baseline</span>
                  <span className="text-sm text-[#737373] tabular-nums">6.6</span>
                </div>
                <div>
                  <span className="text-xs text-[#737373] block">Diff</span>
                  <span className="text-sm font-semibold text-[#171717] tabular-nums">+1.2</span>
                </div>
              </div>
            </div>

            <p className="text-xs text-[#525252] leading-relaxed">
              Undercarriage vibration exceeds nominal operational corridor.
            </p>
          </div>

          {/* Card 4: Safety Discipline */}
          <div className="p-4 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] flex flex-col justify-between space-y-3 shadow-xs">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-[#171717]">Safety discipline</span>
                <Badge variant="safe" size="sm">Superior</Badge>
              </div>

              <div className="grid grid-cols-3 gap-2 my-2.5 py-2.5 border-y border-[#E5E5E5]">
                <div>
                  <span className="text-xs text-[#737373] block">Score</span>
                  <span className="text-sm font-semibold text-[#171717] tabular-nums">{op?.safety_score || 94}%</span>
                </div>
                <div>
                  <span className="text-xs text-[#737373] block">Fleet</span>
                  <span className="text-sm text-[#737373] tabular-nums">{baselines?.fleet_avg_safety || 88}%</span>
                </div>
                <div>
                  <span className="text-xs text-[#737373] block">Diff</span>
                  <span className="text-sm font-semibold text-[#171717] tabular-nums">+6%</span>
                </div>
              </div>
            </div>

            <p className="text-xs text-[#525252] leading-relaxed">
              Operator adherence to safety interlocks is above fleet benchmark.
            </p>
          </div>
        </div>
      </div>

      {/* Anomaly Log Table */}
      <div className="space-y-3">
        <SectionHeader
          title="Explainable anomaly log"
          count={anomalies.length}
          description="Unsupervised anomalies flagged with feature attributions"
        />

        <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] overflow-hidden shadow-xs divide-y divide-[#E5E5E5] text-xs">
          {anomalies.map((anom) => {
            const isCrit = anom.risk_level === 'CRITICAL';
            const isHigh = anom.risk_level === 'HIGH';
            const badgeVariant = isCrit ? 'critical' : isHigh ? 'high' : 'warning';

            return (
              <div key={anom.anomaly_id} className="p-4 hover:bg-[#F5F5F5] transition-colors space-y-1.5">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <Badge variant={badgeVariant} size="sm">
                      {anom.risk_level}
                    </Badge>
                    <span className="font-semibold text-[#171717] font-mono">{anom.anomaly_id}</span>
                    <span className="text-[#737373]">· {anom.machine_id}</span>
                  </div>

                  <div className="text-[#737373] text-xs tabular-nums font-mono">
                    Score: <span className="text-[#171717] font-semibold">{anom.anomaly_score.toFixed(1)}/100</span> · {anom.timestamp?.split('T')[0]}
                  </div>
                </div>

                <p className="text-xs text-[#525252]">
                  {anom.reason}
                </p>

                {anom.factors && anom.factors.length > 0 && (
                  <div className="pt-1 space-y-1 text-xs text-[#737373]">
                    {anom.factors.map((f, i) => (
                      <div key={i} className="flex items-center gap-1.5">
                        <span>•</span>
                        <span>{f}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
