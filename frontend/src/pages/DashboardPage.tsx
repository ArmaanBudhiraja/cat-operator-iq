import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useRole } from '../context/RoleContext';
import { useSimulation } from '../context/SimulationContext';
import { DashboardData } from '../types';
import { ProximityRadar } from '../components/ProximityRadar';
import { TelemetryLiveFeed } from '../components/TelemetryLiveFeed';
import { SafetyAlertBanner } from '../components/SafetyAlertBanner';
import { SimulationControls } from '../components/SimulationControls';
import { SkeletonCard, ErrorState } from '../components/StateViews';
import { Badge } from '../components/ui/Badge';
import { ProgressBar } from '../components/ui/ProgressBar';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const DashboardPage: React.FC = () => {
  const { activeMachineId, activeOperatorId } = useRole();
  const { liveState } = useSimulation();

  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await api.getDashboard(activeOperatorId, activeMachineId);
      setData(res);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to backend service');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, [activeOperatorId, activeMachineId]);

  if (loading) {
    return (
      <div className="space-y-6">
        <SkeletonCard rows={2} />
        <SkeletonCard rows={4} />
      </div>
    );
  }

  if (error || !data) {
    return <ErrorState error={error || 'No dashboard data available'} onRetry={loadDashboard} />;
  }

  const safetyScore = liveState ? liveState.safety_score : data.safety_score;
  const statusLabel = liveState ? liveState.status_label : data.safety_status;
  const riskLevel = liveState ? liveState.risk_level : data.risk_level;
  const activeAlerts = liveState ? liveState.active_alerts : data.active_alerts;
  const radarWorkers = liveState ? liveState.radar_objects : [];

  const taskType = data.current_task ? data.current_task.task_type : 'Earth Excavation';
  const progressPct = data.task_progress_pct || 67;
  const remainingMin = data.estimated_remaining_time_min || 54;

  return (
    <div className="space-y-6 pb-12 max-w-6xl mx-auto font-sans">
      {/* Simulation Controls (Discreet & Collapsible) */}
      <SimulationControls />

      {/* Exception-first Safety Alert Banner */}
      <SafetyAlertBanner
        safetyScore={safetyScore}
        statusLabel={statusLabel}
        riskLevel={riskLevel}
        activeAlerts={activeAlerts}
        disclaimer={data.safety_disclaimer}
        machineId={data.current_machine_id}
      />

      {/* Operational Header */}
      <div>
        <h1 className="text-2xl font-semibold text-[#171717] tracking-tight">
          Dashboard
        </h1>
        <p className="text-xs text-[#737373] mt-0.5">
          Morning shift · {data.current_machine_id} · Operator OP001
        </p>
      </div>

      {/* Current Task Section */}
      <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-5 shadow-xs space-y-4">
        <div className="flex flex-wrap items-baseline justify-between gap-3">
          <div>
            <div className="text-xs font-medium text-[#737373]">
              Current task
            </div>
            <h2 className="text-xl font-semibold text-[#171717] mt-0.5 font-sans">
              {taskType}
            </h2>
            <div className="text-xs text-[#737373] mt-0.5">
              {data.current_machine_id} · Zone A · Task #{data.current_task?.task_id || 'T001'}
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Badge variant="warning" size="md">
              In progress
            </Badge>
          </div>
        </div>

        {/* Prediction & Progress Bar */}
        <div className="space-y-1.5 pt-1">
          <div className="flex items-baseline justify-between">
            <span className="text-xs text-[#525252]">
              Predicted completion
            </span>
            <span className="text-2xl font-semibold text-[#171717] tabular-nums font-sans">
              {remainingMin} min
            </span>
          </div>

          <ProgressBar
            value={progressPct}
            label="Progress"
            showPercent={true}
            size="xs"
          />
        </div>

        {/* Operating Conditions Triad */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 border-t border-[#E5E5E5] text-xs">
          <div>
            <span className="text-xs text-[#737373] block">Weather</span>
            <span className="text-[#171717] font-medium text-sm mt-0.5 block">{data.weather.condition}</span>
            <span className="text-[#737373] text-xs tabular-nums">{data.weather.temperature_c}°C · {data.weather.wind_speed_kmh} km/h</span>
          </div>

          <div>
            <span className="text-xs text-[#737373] block">Machine health</span>
            <span className="text-[#171717] font-medium text-sm mt-0.5 block tabular-nums">{data.machine_health_pct} / 100</span>
            <span className="text-[#525252] text-xs">Nominal operating corridor</span>
          </div>

          <div>
            <span className="text-xs text-[#737373] block">Safety status</span>
            <span className="text-[#171717] font-medium text-sm mt-0.5 block">{statusLabel}</span>
            <span className="text-[#737373] text-xs tabular-nums">Score {safetyScore.toFixed(0)} / 100</span>
          </div>
        </div>
      </div>

      {/* Today's Performance Summary Bar */}
      <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-5 shadow-xs">
        <div className="text-xs font-medium text-[#737373] mb-3">
          Today's performance
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 divide-y md:divide-y-0 md:divide-x divide-[#E5E5E5] pt-1">
          <div className="py-2 md:py-0 md:pr-4">
            <div className="text-xs text-[#525252]">
              Task efficiency
            </div>
            <div className="text-2xl font-semibold text-[#171717] mt-1 tabular-nums">
              {Math.round(((data.kpis.completed_tasks || 2) / (data.kpis.today_tasks || 3)) * 100) || 78}%
            </div>
            <div className="text-xs text-[#737373] mt-1">
              {data.kpis.completed_tasks} of {data.kpis.today_tasks} completed
            </div>
          </div>

          <div className="py-2 md:py-0 md:px-4">
            <div className="text-xs text-[#525252]">
              Machine utilization
            </div>
            <div className="text-2xl font-semibold text-[#171717] mt-1 tabular-nums">
              {data.kpis.machine_utilization.toFixed(0)}%
            </div>
            <div className="text-xs text-[#737373] mt-1">
              Active productive runtime
            </div>
          </div>

          <div className="py-2 md:py-0 md:px-4">
            <div className="text-xs text-[#525252]">
              Idle time
            </div>
            <div className="text-2xl font-semibold text-[#171717] mt-1 tabular-nums">
              {data.kpis.idle_time_min.toFixed(0)} <span className="text-xs font-normal text-[#737373]">min</span>
            </div>
            <div className="text-xs text-[#737373] mt-1">
              Baseline: 27 min
            </div>
          </div>

          <div className="py-2 md:py-0 md:pl-4">
            <div className="text-xs text-[#525252]">
              Safety score
            </div>
            <div className="text-2xl font-semibold text-[#171717] mt-1 tabular-nums">
              {safetyScore.toFixed(0)}
            </div>
            <div className="text-xs text-[#737373] mt-1">
              8 rules evaluated
            </div>
          </div>
        </div>
      </div>

      {/* Proximity Perimeter Visualization */}
      <ProximityRadar workers={radarWorkers} machineId={data.current_machine_id} />

      {/* Real-time Sensor Telemetry Stream */}
      {liveState && <TelemetryLiveFeed telemetry={liveState.telemetry} />}

      {/* Operational Shortcuts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 text-xs">
        <Link
          to="/tasks"
          className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] hover:border-[#D4D4D4] hover:bg-[#FAFAFA] transition-colors flex items-center justify-between group shadow-xs"
        >
          <div>
            <div className="text-xs text-[#737373]">Operational queue</div>
            <div className="text-xs font-semibold text-[#171717] mt-0.5">
              Tasks & ML predictions
            </div>
          </div>
          <ArrowRight className="w-4 h-4 text-[#737373] group-hover:text-[#171717] transition-colors" />
        </Link>

        <Link
          to="/behavior"
          className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] hover:border-[#D4D4D4] hover:bg-[#FAFAFA] transition-colors flex items-center justify-between group shadow-xs"
        >
          <div>
            <div className="text-xs text-[#737373]">Behavior analytics</div>
            <div className="text-xs font-semibold text-[#171717] mt-0.5">
              Baseline deviations
            </div>
          </div>
          <ArrowRight className="w-4 h-4 text-[#737373] group-hover:text-[#171717] transition-colors" />
        </Link>

        <Link
          to="/assistant"
          className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] hover:border-[#D4D4D4] hover:bg-[#FAFAFA] transition-colors flex items-center justify-between group shadow-xs"
        >
          <div>
            <div className="text-xs text-[#737373]">Operational assistant</div>
            <div className="text-xs font-semibold text-[#171717] mt-0.5">
              OperatorIQ Intelligence
            </div>
          </div>
          <ArrowRight className="w-4 h-4 text-[#737373] group-hover:text-[#171717] transition-colors" />
        </Link>
      </div>
    </div>
  );
};
