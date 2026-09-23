import React from 'react';
import { SafetyAlert } from '../types';
import { ArrowRight, Info } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Badge } from './ui/Badge';
import { Button } from './ui/Button';

interface SafetyAlertBannerProps {
  safetyScore: number;
  statusLabel: string;
  riskLevel: string;
  activeAlerts: SafetyAlert[];
  disclaimer?: string;
  machineId?: string;
}

export const SafetyAlertBanner: React.FC<SafetyAlertBannerProps> = ({
  safetyScore,
  riskLevel,
  activeAlerts = [],
  disclaimer = "AI-generated recommendations are advisory and must not replace official operating procedures, safety procedures, operator training, or professional judgment.",
  machineId = 'EXC001',
}) => {
  const isCritical = riskLevel === 'CRITICAL' || activeAlerts.some((a) => a.severity === 'CRITICAL');
  const isHigh = riskLevel === 'HIGH' || activeAlerts.some((a) => a.severity === 'HIGH');
  const hasAlerts = activeAlerts.length > 0 || isCritical || isHigh;

  // When system is nominal: visually quiet, clear ribbon
  if (!hasAlerts) {
    return (
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3 px-4 py-2.5 bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] text-xs shadow-xs font-sans">
        <div className="flex items-center gap-2.5">
          <span className="w-2 h-2 rounded-full bg-[#525252]"></span>
          <span className="text-[#171717] font-semibold text-xs">
            Normal operations
          </span>
          <span className="text-[#D4D4D4]">|</span>
          <span className="text-[#525252]">
            {machineId} perimeter nominal
          </span>
          <span className="text-[#D4D4D4]">|</span>
          <span className="text-[#525252]">
            Safety score: <strong className="text-[#171717] font-semibold tabular-nums">{safetyScore.toFixed(0)}/100</strong>
          </span>
        </div>

        <div className="flex items-center gap-3 text-xs text-[#737373]">
          <span className="hidden sm:inline">Telemetry & LiDAR active</span>
          <Link
            to="/safety"
            className="text-[#171717] hover:underline transition-colors flex items-center gap-1 font-medium"
          >
            <span>Safety Center</span>
            <ArrowRight className="w-3 h-3" />
          </Link>
        </div>
      </div>
    );
  }

  // When an event occurs: Clean, strong monochrome panel
  const primaryAlert = activeAlerts[0] || {
    title: isCritical ? 'Critical proximity hazard detected' : 'Proximity hazard detected',
    message: isCritical ? `Worker detected 2.3m from ${machineId}` : `Proximity warning active on ${machineId}`,
    severity: isCritical ? 'CRITICAL' : 'HIGH',
    rule_id: 'RULE_PROXIMITY_HAZARD',
  };

  const alertBadgeVariant = isCritical ? 'critical' : isHigh ? 'high' : 'warning';

  return (
    <div
      role="alert"
      className={`mb-5 p-5 rounded-[6px] bg-[#FFFFFF] transition-all ${
        isCritical
          ? 'border-2 border-[#111111] shadow-xs'
          : 'border border-[#171717]'
      }`}
    >
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold tracking-tight text-[#171717] font-sans">
              {isCritical ? 'Critical event' : 'Attention required'}
            </span>
            <Badge variant={alertBadgeVariant}>
              {primaryAlert.severity || riskLevel}
            </Badge>
          </div>

          <h3 className="text-base font-semibold text-[#171717] font-sans">
            {primaryAlert.title}
          </h3>

          <p className="text-sm text-[#525252] max-w-2xl font-sans leading-relaxed">
            {primaryAlert.message}
          </p>

          <div className="text-xs text-[#737373] pt-0.5 font-sans">
            Detected 12 seconds ago · Rule: {primaryAlert.rule_id || 'PROX_01'}
          </div>
        </div>

        <div className="shrink-0 flex items-center sm:items-start">
          <Link to="/safety">
            <Button
              variant="primary"
              size="md"
              icon={<ArrowRight className="w-3.5 h-3.5" />}
            >
              Review event
            </Button>
          </Link>
        </div>
      </div>

      {/* Advisory Disclaimer */}
      <div className="mt-4 pt-2.5 border-t border-[#E5E5E5] flex items-center gap-2 text-xs text-[#737373] font-sans">
        <Info className="w-3.5 h-3.5 text-[#737373] shrink-0" />
        <span>{disclaimer}</span>
      </div>
    </div>
  );
};
