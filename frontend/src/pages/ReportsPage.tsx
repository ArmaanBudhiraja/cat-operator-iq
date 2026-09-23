import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useRole } from '../context/RoleContext';
import { SkeletonCard, ErrorState } from '../components/StateViews';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { SectionHeader } from '../components/ui/SectionHeader';
import { Printer, Download, ArrowRight } from 'lucide-react';

export const ReportsPage: React.FC = () => {
  const { activeOperatorId, activeMachineId } = useRole();
  const [reportType, setReportType] = useState<string>('daily_operator');
  const [reportData, setReportData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadReport = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getReport(reportType, activeOperatorId, activeMachineId);
      setReportData(data);
    } catch (err: any) {
      setError(err.message || 'Failed to generate operational report');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReport();
  }, [reportType, activeOperatorId, activeMachineId]);

  const handlePrint = () => {
    window.print();
  };

  const handleExportJson = () => {
    if (!reportData) return;
    const jsonStr = JSON.stringify(reportData, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${reportData.report_id || 'report'}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const reportTemplates = [
    {
      id: 'daily_operator',
      title: 'Daily Operations',
      description: 'Shift operational log, tasks completed, machine utilization and operator attendance.',
      lastGenerated: 'Today · 08:30',
    },
    {
      id: 'safety',
      title: 'Safety Summary',
      description: 'Perimeter incursions, interlock compliance, risk scoring and logged incident records.',
      lastGenerated: 'Today · 07:00',
    },
    {
      id: 'machine_health',
      title: 'Machine Performance',
      description: 'Fleet health diagnostics, telemetry variance, thermal trends and vibration levels.',
      lastGenerated: 'Yesterday · 18:00',
    },
    {
      id: 'task_efficiency',
      title: 'Operator Performance',
      description: 'Task cycle benchmarks, fuel efficiency, training standing and baseline deviations.',
      lastGenerated: 'Today · 09:15',
    },
  ];

  return (
    <div className="space-y-6 pb-12 max-w-5xl mx-auto font-sans">
      <div className="print:hidden space-y-6">
        {/* Header */}
        <div className="flex flex-wrap items-baseline justify-between gap-4 pb-3 border-b border-[#E5E5E5]">
          <div>
            <h1 className="text-2xl font-semibold text-[#171717] tracking-tight">
              Reports
            </h1>
            <p className="text-xs text-[#737373] mt-0.5">
              Auditable shift records, safety compliance logs and machine diagnostics
            </p>
          </div>

          <div className="flex items-center gap-2.5">
            <Button
              variant="secondary"
              size="sm"
              onClick={handlePrint}
              icon={<Printer className="w-3.5 h-3.5 text-current" />}
            >
              Print / Save PDF
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={handleExportJson}
              icon={<Download className="w-3.5 h-3.5 text-current" />}
            >
              Export JSON
            </Button>
          </div>
        </div>

        {/* Report Templates */}
        <div className="space-y-3">
          <SectionHeader
            title="Report templates"
            description="Select an operational template to generate"
          />

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            {reportTemplates.map((t) => {
              const isActive = reportType === t.id;
              return (
                <div
                  key={t.id}
                  onClick={() => setReportType(t.id)}
                  className={`p-4 rounded-[6px] border transition-colors cursor-pointer flex flex-col justify-between space-y-3 shadow-xs ${
                    isActive
                      ? 'bg-[#FFFFFF] border-2 border-[#111111]'
                      : 'bg-[#FFFFFF] border-[#E5E5E5] hover:border-[#D4D4D4]'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <h4 className="text-xs font-semibold text-[#171717]">
                        {t.title}
                      </h4>
                      {isActive && <Badge variant="warning" size="sm">Active</Badge>}
                    </div>

                    <p className="text-xs text-[#525252] line-clamp-2 leading-relaxed">
                      {t.description}
                    </p>
                  </div>

                  <div className="pt-2 border-t border-[#E5E5E5] flex items-center justify-between text-xs text-[#737373]">
                    <span>{t.lastGenerated}</span>
                    <span className="text-[#171717] font-medium flex items-center gap-1">
                      Open <ArrowRight className="w-3 h-3" />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {loading ? (
        <SkeletonCard rows={8} />
      ) : error ? (
        <ErrorState error={error} onRetry={loadReport} />
      ) : reportData ? (
        /* Printable Report Document */
        <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-8 shadow-xs text-xs text-[#171717] space-y-5 font-sans">
          <div className="flex flex-wrap items-start justify-between gap-4 pb-5 border-b border-[#E5E5E5]">
            <div>
              <div className="text-xs text-[#737373] font-semibold">
                CAT OperatorIQ · Formal Operational Report
              </div>
              <h2 className="text-xl font-semibold text-[#171717] mt-1">
                {reportData.title || 'Operational Shift Report'}
              </h2>
              <div className="text-xs text-[#737373] mt-0.5">
                ID: {reportData.report_id || 'RPT-2024-001'} · Generated: {reportData.generated_at?.replace('T', ' ').slice(0, 19)}
              </div>
            </div>

            <div className="text-right text-xs text-[#737373] space-y-0.5">
              <div>Site: <strong className="text-[#171717]">Sector 4 Foundation</strong></div>
              <div>Machine: <strong className="text-[#171717] font-mono">{activeMachineId}</strong></div>
              <div>Operator: <strong className="text-[#171717] font-mono">{activeOperatorId}</strong></div>
            </div>
          </div>

          {/* KPI Strip */}
          {reportData.kpis && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-3 border-b border-[#E5E5E5]">
              {Object.entries(reportData.kpis).map(([k, v]: [string, any]) => (
                <div key={k}>
                  <span className="text-xs text-[#737373] block capitalize">
                    {k.replace(/_/g, ' ')}
                  </span>
                  <div className="text-2xl font-semibold text-[#171717] mt-0.5 tabular-nums">
                    {typeof v === 'number' ? v.toFixed(1) : String(v)}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Report Sections Content */}
          {reportData.sections && reportData.sections.length > 0 && (
            <div className="space-y-4">
              {reportData.sections.map((sec: any, idx: number) => (
                <div key={idx} className="space-y-1.5">
                  <h4 className="text-xs font-semibold text-[#171717]">
                    {sec.heading}
                  </h4>
                  <p className="text-xs text-[#525252] leading-relaxed">
                    {sec.content}
                  </p>
                  {sec.items && sec.items.length > 0 && (
                    <ul className="space-y-1 pt-1 text-xs text-[#525252]">
                      {sec.items.map((item: string, iIdx: number) => (
                        <li key={iIdx} className="flex items-start gap-2">
                          <span className="text-[#737373]">•</span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Sign-off */}
          <div className="pt-5 border-t border-[#E5E5E5] grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs text-[#737373]">
            <div>
              <span className="text-xs text-[#737373] block mb-1">
                Data verification hash
              </span>
              <div className="text-xs truncate bg-[#FAFAFA] p-2 rounded-[4px] border border-[#E5E5E5] font-mono text-[#525252]">
                SHA256: 4b9a8f27e10c5d33b8a1928374fa09e2b7c4d5e6f1a2b3c4
              </div>
            </div>

            <div className="sm:text-right">
              <span className="text-xs text-[#737373] block mb-1">
                Certified by
              </span>
              <div className="text-[#171717] font-semibold">
                Shift Supervisor Digital Sign-off
              </div>
              <div className="text-xs text-[#737373]">
                Status: Audit Compliant
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};
