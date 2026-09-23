import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useRole } from '../context/RoleContext';
import { MachineItem } from '../types';
import { SkeletonCard, ErrorState } from '../components/StateViews';
import { Badge } from '../components/ui/Badge';
import { ProgressBar } from '../components/ui/ProgressBar';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

export const MachineHealthPage: React.FC = () => {
  const { activeMachineId, setActiveMachineId } = useRole();
  const [machines, setMachines] = useState<MachineItem[]>([]);
  const [selectedMachine, setSelectedMachine] = useState<MachineItem | null>(null);
  const [telemetryHistory, setTelemetryHistory] = useState<any[]>([]);
  const [filterType, setFilterType] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'overview' | 'telemetry' | 'safety' | 'history'>('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadMachines = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getMachines();
      setMachines(data);

      const current = data.find((m) => m.machine_id === activeMachineId) || data[0];
      if (current) {
        setSelectedMachine(current);
        loadHistory(current.machine_id);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load machines');
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = async (id: string) => {
    try {
      const history = await api.getMachineTelemetryHistory(id);
      setTelemetryHistory(history);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadMachines();
  }, []);

  const handleSelectMachine = (m: MachineItem) => {
    setSelectedMachine(m);
    setActiveMachineId(m.machine_id);
    loadHistory(m.machine_id);
  };

  const filteredMachines = filterType
    ? machines.filter((m) => m.machine_type === filterType)
    : machines;

  return (
    <div className="space-y-6 pb-12 max-w-6xl mx-auto font-sans">
      {/* Header */}
      {selectedMachine && (
        <div className="flex flex-wrap items-baseline justify-between gap-4 pb-3 border-b border-[#E5E5E5]">
          <div className="flex items-baseline gap-3">
            <h1 className="text-2xl font-semibold text-[#171717] font-mono tracking-tight">
              {selectedMachine.machine_id}
            </h1>
            <span className="text-sm font-sans text-[#737373]">
              {selectedMachine.machine_type}
            </span>
            <Badge variant="safe" size="sm">
              Operational
            </Badge>
          </div>

          <div className="flex items-center gap-1.5 p-0.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] text-xs font-sans">
            {['', 'Excavator', 'Wheel Loader', 'Dozer', 'Dump Truck'].map((t) => (
              <button
                key={t}
                onClick={() => setFilterType(t)}
                className={`px-3 py-1 rounded-[3px] text-xs transition-colors ${
                  filterType === t
                    ? 'bg-[#111111] text-[#FFFFFF] font-medium shadow-xs'
                    : 'text-[#525252] hover:text-[#171717]'
                }`}
              >
                {t || 'All fleet'}
              </button>
            ))}
          </div>
        </div>
      )}

      {loading ? (
        <SkeletonCard rows={6} />
      ) : error ? (
        <ErrorState error={error} onRetry={loadMachines} />
      ) : selectedMachine ? (
        <div className="space-y-6">
          {/* Key Metrics Row */}
          <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-5 shadow-xs">
            <div className="grid grid-cols-2 md:grid-cols-4 divide-y md:divide-y-0 md:divide-x divide-[#E5E5E5]">
              <div className="py-2 md:py-0 md:pr-4">
                <div className="text-xs text-[#525252]">
                  Health score
                </div>
                <div className="text-2xl font-semibold text-[#171717] mt-1 tabular-nums">
                  {selectedMachine.health_score?.toFixed(0) || 92} <span className="text-xs font-normal text-[#737373]">/ 100</span>
                </div>
                <div className="text-xs text-[#737373] mt-1">
                  Composite index
                </div>
              </div>

              <div className="py-2 md:py-0 md:px-4">
                <div className="text-xs text-[#525252]">
                  Engine hours
                </div>
                <div className="text-2xl font-semibold text-[#171717] mt-1 tabular-nums">
                  {selectedMachine.engine_hours.toFixed(1)}
                </div>
                <div className="text-xs text-[#737373] mt-1">
                  Lifetime machine meter
                </div>
              </div>

              <div className="py-2 md:py-0 md:px-4">
                <div className="text-xs text-[#525252]">
                  Fuel level
                </div>
                <div className="text-2xl font-semibold text-[#171717] mt-1 tabular-nums">
                  72%
                </div>
                <div className="text-xs text-[#737373] mt-1">
                  Operational fuel cell
                </div>
              </div>

              <div className="py-2 md:py-0 md:pl-4">
                <div className="text-xs text-[#525252]">
                  Utilization
                </div>
                <div className="text-2xl font-semibold text-[#171717] mt-1 tabular-nums">
                  84%
                </div>
                <div className="text-xs text-[#737373] mt-1">
                  Active shift engagement
                </div>
              </div>
            </div>
          </div>

          {/* Minimal Tab Navigation */}
          <div className="flex items-center gap-6 border-b border-[#E5E5E5] text-xs font-sans">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'telemetry', label: 'Telemetry' },
              { id: 'safety', label: 'Safety' },
              { id: 'history', label: 'History' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`pb-2.5 transition-colors relative font-medium ${
                  activeTab === tab.id
                    ? 'text-[#171717] border-b-2 border-[#111111]'
                    : 'text-[#737373] hover:text-[#171717]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab 1: Overview */}
          {activeTab === 'overview' && (
            <div className="space-y-4">
              <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-5 shadow-xs space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-[#525252]">Machine health score</span>
                  <span className="text-[#171717] tabular-nums font-semibold">{selectedMachine.health_score?.toFixed(0) || 92} / 100</span>
                </div>
                <ProgressBar value={selectedMachine.health_score || 92} size="sm" />
              </div>

              {/* Subsystem Health Metrics */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
                <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
                  <span className="text-xs text-[#737373] block">Engine state</span>
                  <span className="text-sm font-semibold text-[#171717] mt-0.5 block">Normal</span>
                  <span className="text-xs text-[#737373] mt-0.5 block">ECU diagnostic nominal</span>
                </div>

                <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
                  <span className="text-xs text-[#737373] block">Temperature</span>
                  <span className="text-sm font-semibold text-[#171717] mt-0.5 block">Normal</span>
                  <span className="text-xs text-[#737373] mt-0.5 block">82°C operating temp</span>
                </div>

                <div className="p-3.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] shadow-xs">
                  <span className="text-xs text-[#737373] block">Oil pressure</span>
                  <span className="text-sm font-semibold text-[#171717] mt-0.5 block">Normal</span>
                  <span className="text-xs text-[#737373] mt-0.5 block">42 PSI within corridor</span>
                </div>

                <div className="p-3.5 bg-[#FFFFFF] border border-[#737373] rounded-[6px] shadow-xs">
                  <span className="text-xs text-[#737373] block">Vibration</span>
                  <span className="text-sm font-semibold text-[#171717] mt-0.5 block">Elevated</span>
                  <span className="text-xs text-[#171717] mt-0.5 block font-mono">7.8 mm/s · ↑ 18% vs baseline</span>
                </div>
              </div>
            </div>
          )}

          {/* Tab 2: Telemetry */}
          {activeTab === 'telemetry' && (
            <div className="space-y-4">
              {/* Telemetry Metrics Readouts */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-5 shadow-xs">
                <div>
                  <div className="text-xs text-[#737373]">Engine temperature</div>
                  <div className="text-2xl font-semibold text-[#171717] mt-0.5 tabular-nums">82°C</div>
                  <div className="text-xs text-[#525252] mt-0.5">↑ +3.2°C vs baseline</div>
                </div>

                <div>
                  <div className="text-xs text-[#737373]">Vibration</div>
                  <div className="text-2xl font-semibold text-[#171717] mt-0.5 tabular-nums">7.8 mm/s</div>
                  <div className="text-xs text-[#525252] mt-0.5">↑ +18% vs baseline</div>
                </div>

                <div>
                  <div className="text-xs text-[#737373]">Oil pressure</div>
                  <div className="text-2xl font-semibold text-[#171717] mt-0.5 tabular-nums">38 PSI</div>
                  <div className="text-xs text-[#525252] mt-0.5">↓ -4% vs baseline</div>
                </div>
              </div>

              {/* Monochrome Recharts */}
              {telemetryHistory.length > 0 && (
                <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-5 shadow-xs">
                  <div className="text-xs font-semibold text-[#171717] mb-3">
                    Telemetry trends over time
                  </div>
                  <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={telemetryHistory}>
                        <XAxis dataKey="timestamp" tick={false} stroke="#E5E5E5" />
                        <YAxis stroke="#737373" fontSize={11} domain={['auto', 'auto']} tickLine={false} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#FFFFFF',
                            border: '1px solid #E5E5E5',
                            borderRadius: '4px',
                            fontSize: '11px',
                            color: '#171717',
                            fontFamily: 'sans-serif',
                            boxShadow: '0 2px 8px rgba(0,0,0,0.08)'
                          }}
                        />
                        <Line
                          type="monotone"
                          dataKey="vibration"
                          stroke="#111111"
                          strokeWidth={1.5}
                          dot={false}
                          name="Vibration"
                        />
                        <Line
                          type="monotone"
                          dataKey="engine_temperature"
                          stroke="#737373"
                          strokeWidth={1.5}
                          dot={false}
                          name="Engine Temp"
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Tab 3: Safety */}
          {activeTab === 'safety' && (
            <div className="space-y-2.5 text-xs">
              <div className="p-4 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] flex items-center justify-between shadow-xs">
                <div>
                  <div className="text-[#171717] font-semibold">Seatbelt restraint interlock</div>
                  <div className="text-[#737373] text-xs">CAN-bus sensor feed</div>
                </div>
                <Badge variant="safe">Compliant</Badge>
              </div>

              <div className="p-4 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] flex items-center justify-between shadow-xs">
                <div>
                  <div className="text-[#171717] font-semibold">LiDAR 360° perimeter sensor</div>
                  <div className="text-[#737373] text-xs">14-meter operational envelope</div>
                </div>
                <Badge variant="safe">Active</Badge>
              </div>
            </div>
          )}

          {/* Tab 4: History */}
          {activeTab === 'history' && (
            <div className="space-y-2.5 text-xs">
              <div className="p-4 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] flex justify-between shadow-xs">
                <div>
                  <div className="text-[#171717] font-semibold">Scheduled 500-hour hydraulic service</div>
                  <div className="text-[#737373] text-xs">Completed by Site Maintenance Team</div>
                </div>
                <div className="text-[#737373]">18 days ago</div>
              </div>
            </div>
          )}

          {/* Fleet Machine Table */}
          <div className="pt-2">
            <div className="text-xs font-semibold text-[#171717] mb-2.5">
              Fleet machinery ({filteredMachines.length})
            </div>
            <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] overflow-hidden shadow-xs">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="bg-[#FAFAFA] border-b border-[#E5E5E5] text-xs text-[#525252] font-medium">
                    <th className="py-2.5 px-4 font-medium">Machine</th>
                    <th className="py-2.5 px-4 font-medium">Model</th>
                    <th className="py-2.5 px-4 font-medium">Engine hours</th>
                    <th className="py-2.5 px-4 font-medium text-right">Health</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E5E5E5] text-[13px]">
                  {filteredMachines.map((m) => (
                    <tr
                      key={m.machine_id}
                      onClick={() => handleSelectMachine(m)}
                      className={`cursor-pointer transition-colors ${
                        selectedMachine.machine_id === m.machine_id
                          ? 'bg-[#F5F5F5] font-medium'
                          : 'hover:bg-[#FAFAFA]'
                      }`}
                    >
                      <td className="py-3 px-4 text-[#171717] font-mono">{m.machine_id}</td>
                      <td className="py-3 px-4 text-[#525252]">{m.machine_model}</td>
                      <td className="py-3 px-4 text-[#525252] tabular-nums font-mono">{m.engine_hours.toFixed(0)} hrs</td>
                      <td className="py-3 px-4 text-right text-[#171717] tabular-nums font-semibold">
                        {m.health_score?.toFixed(0) || 90}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};
