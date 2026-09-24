import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useRole } from '../context/RoleContext';
import { IncidentItem } from '../types';
import { IncidentModal } from '../components/IncidentModal';
import { SkeletonCard, ErrorState, EmptyState } from '../components/StateViews';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Drawer } from '../components/ui/Drawer';
import { Plus, Check } from 'lucide-react';
import { formatIncidentTableTime, formatIncidentDetailTime } from '../utils/dateFormat';

export const IncidentsPage: React.FC = () => {
  const { activeMachineId, activeOperatorId } = useRole();
  const [incidents, setIncidents] = useState<IncidentItem[]>([]);
  const [selectedIncident, setSelectedIncident] = useState<IncidentItem | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [filterSeverity, setFilterSeverity] = useState<string>('');
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [resolving, setResolving] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const list = await api.getIncidents(filterSeverity || undefined);
      setIncidents(list);
    } catch (err: any) {
      setError(err.message || 'Failed to load incidents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [filterSeverity]);

  const handleResolve = async (incidentId: string) => {
    setResolving(true);
    try {
      await api.updateIncident(incidentId, true, "Remediation verified by shift supervisor.");
      if (selectedIncident && selectedIncident.incident_id === incidentId) {
        setSelectedIncident({ ...selectedIncident, resolved: true, resolution: "Remediation verified by shift supervisor." });
      }
      await loadData();
    } catch (e) {
      console.error(e);
    } finally {
      setResolving(false);
    }
  };

  const handleRowClick = (inc: IncidentItem) => {
    setSelectedIncident(inc);
    setDrawerOpen(true);
  };

  return (
    <div className="space-y-6 pb-12 max-w-6xl mx-auto font-sans">
      {/* Header */}
      <div className="flex flex-wrap items-baseline justify-between gap-4 pb-3 border-b border-[#E5E5E5]">
        <div>
          <h1 className="text-2xl font-semibold text-[#171717] tracking-tight">
            Incidents
          </h1>
          <p className="text-xs text-[#737373] mt-0.5">
            Auditable incident database and supervisor sign-off · {incidents.length} records
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 p-0.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[4px] text-xs">
            {['', 'Critical', 'High', 'Medium', 'Low'].map((sev) => (
              <button
                key={sev}
                onClick={() => setFilterSeverity(sev)}
                className={`px-3 py-1 rounded-[3px] text-xs transition-colors ${
                  filterSeverity === sev
                    ? 'bg-[#111111] text-[#FFFFFF] font-medium shadow-xs'
                    : 'text-[#525252] hover:text-[#171717]'
                }`}
              >
                {sev || 'All'}
              </button>
            ))}
          </div>

          <Button
            variant="primary"
            size="sm"
            onClick={() => setShowModal(true)}
            icon={<Plus className="w-3.5 h-3.5 text-current" />}
          >
            Log incident
          </Button>
        </div>
      </div>

      {loading ? (
        <SkeletonCard rows={6} />
      ) : error ? (
        <ErrorState error={error} onRetry={loadData} />
      ) : incidents.length === 0 ? (
        <EmptyState
          title="No active incidents"
          message="Everything is quiet. No incidents logged matching the active filters."
          actionLabel="Clear filter"
          onAction={() => setFilterSeverity('')}
        />
      ) : (
        /* Incident Table */
        <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] overflow-x-auto shadow-xs">
          <table className="w-full border-collapse text-left">
            <thead>
              <tr className="bg-[#FAFAFA] border-b border-[#E5E5E5] text-xs text-[#525252] font-medium">
                <th className="py-2.5 px-4 font-medium">Severity</th>
                <th className="py-2.5 px-4 font-medium">Type</th>
                <th className="py-2.5 px-4 font-medium">Machine</th>
                <th className="py-2.5 px-4 font-medium">Operator</th>
                <th className="py-2.5 px-4 font-medium text-right">Time</th>
                <th className="py-2.5 px-4 font-medium text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E5E5] text-[13px]">
              {incidents.map((inc) => {
                const sev = inc.severity.toLowerCase();
                const badgeVariant = sev === 'critical' ? 'critical' : sev === 'high' ? 'high' : sev === 'medium' ? 'warning' : 'safe';

                return (
                  <tr
                    key={inc.incident_id}
                    onClick={() => handleRowClick(inc)}
                    className="cursor-pointer hover:bg-[#F5F5F5] transition-colors"
                  >
                    <td className="py-3 px-4">
                      <Badge variant={badgeVariant} size="sm">
                        {inc.severity}
                      </Badge>
                    </td>

                    <td className="py-3 px-4 text-[#171717] font-medium">
                      {inc.incident_type}
                      <span className="block text-xs text-[#737373] font-mono mt-0.5 font-normal">
                        #{inc.incident_id}
                      </span>
                    </td>

                    <td className="py-3 px-4 text-[#171717] font-mono text-xs">
                      {inc.machine_id}
                    </td>

                    <td className="py-3 px-4 text-[#525252] font-mono text-xs">
                      {inc.operator_id}
                    </td>

                    <td className="py-3 px-4 text-right text-[#737373] tabular-nums font-mono text-xs">
                      {formatIncidentTableTime(inc.timestamp)}
                    </td>

                    <td className="py-3 px-4 text-right">
                      {inc.resolved ? (
                        <span className="text-[#525252] text-xs font-medium">
                          Resolved
                        </span>
                      ) : (
                        <span className="text-[#171717] text-xs font-semibold">
                          Open
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Incident Detail Drawer */}
      <Drawer
        isOpen={drawerOpen && !!selectedIncident}
        onClose={() => setDrawerOpen(false)}
        title={selectedIncident?.incident_type || 'Incident details'}
        subtitle={`Incident #${selectedIncident?.incident_id} · Machine: ${selectedIncident?.machine_id}`}
        width="max-w-[460px]"
      >
        {selectedIncident && (
          <div className="space-y-5 text-xs font-sans">
            <div className="flex items-center justify-between p-3.5 bg-[#FAFAFA] border border-[#E5E5E5] rounded-[4px]">
              <div className="flex items-center gap-2">
                <span className="text-[#737373] text-xs">Severity:</span>
                <Badge
                  variant={
                    selectedIncident.severity.toLowerCase() === 'critical'
                      ? 'critical'
                      : selectedIncident.severity.toLowerCase() === 'high'
                      ? 'high'
                      : 'warning'
                  }
                >
                  {selectedIncident.severity}
                </Badge>
              </div>

              <div>
                {selectedIncident.resolved ? (
                  <span className="text-[#171717] text-xs font-medium">
                    Verified resolved
                  </span>
                ) : (
                  <Button
                    variant="primary"
                    size="sm"
                    loading={resolving}
                    onClick={() => handleResolve(selectedIncident.incident_id)}
                    icon={<Check className="w-3.5 h-3.5 text-current" />}
                  >
                    Mark resolved
                  </Button>
                )}
              </div>
            </div>

            <div className="space-y-2.5 py-3 border-y border-[#E5E5E5]">
              <div className="flex justify-between">
                <span className="text-[#737373]">Machine</span>
                <span className="text-[#171717] font-medium font-mono">{selectedIncident.machine_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#737373]">Operator</span>
                <span className="text-[#171717] font-mono">{selectedIncident.operator_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#737373]">Location</span>
                <span className="text-[#171717] truncate max-w-[240px]">{selectedIncident.location}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#737373]">Timestamp</span>
                <span className="text-[#737373] tabular-nums font-mono">{formatIncidentDetailTime(selectedIncident.timestamp)}</span>
              </div>
            </div>

            <div className="space-y-1.5">
              <span className="text-xs font-semibold text-[#171717]">
                Incident description
              </span>
              <p className="text-xs text-[#525252] leading-relaxed p-3.5 bg-[#FAFAFA] border border-[#E5E5E5] rounded-[4px]">
                {selectedIncident.description}
              </p>
            </div>

            {selectedIncident.resolution && (
              <div className="space-y-1.5">
                <span className="text-xs font-semibold text-[#171717]">
                  Resolution sign-off
                </span>
                <p className="text-xs text-[#171717] p-3.5 bg-[#FAFAFA] border border-[#E5E5E5] rounded-[4px]">
                  {selectedIncident.resolution}
                </p>
              </div>
            )}
          </div>
        )}
      </Drawer>

      {/* Incident Modal */}
      {showModal && (
        <IncidentModal
          onClose={() => setShowModal(false)}
          onSuccess={loadData}
          defaultMachineId={activeMachineId}
          defaultOperatorId={activeOperatorId}
        />
      )}
    </div>
  );
};
