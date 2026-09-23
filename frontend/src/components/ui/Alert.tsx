import React from 'react';
import { AlertCircle, AlertTriangle, Shield, X } from 'lucide-react';

export type AlertSeverity = 'safe' | 'warning' | 'high' | 'critical' | 'info' | 'normal';

interface AlertProps {
  severity: AlertSeverity;
  title: string;
  description?: React.ReactNode;
  action?: React.ReactNode;
  timestamp?: string;
  onDismiss?: () => void;
  className?: string;
}

export const Alert: React.FC<AlertProps> = ({
  severity,
  title,
  description,
  action,
  timestamp,
  onDismiss,
  className = '',
}) => {
  const isCritical = severity === 'critical';
  const isHigh = severity === 'high';
  const isWarning = severity === 'warning';

  const borderClass = isCritical
    ? 'border-2 border-[#111111] bg-[#FFFFFF] shadow-xs'
    : isHigh
    ? 'border border-[#171717] bg-[#FAFAFA]'
    : isWarning
    ? 'border border-[#737373] bg-[#FAFAFA]'
    : 'border border-[#E5E5E5] bg-[#FFFFFF]';

  return (
    <div
      className={`rounded-[6px] ${borderClass} p-4 transition-colors ${className}`}
      role="alert"
    >
      <div className="flex items-start gap-3">
        <div className="mt-0.5 shrink-0 text-[#171717]">
          {isCritical ? (
            <AlertCircle className="w-4 h-4 text-[#111111]" />
          ) : isHigh || isWarning ? (
            <AlertTriangle className="w-4 h-4 text-[#525252]" />
          ) : (
            <Shield className="w-4 h-4 text-[#737373]" />
          )}
        </div>

        <div className="min-w-0 flex-1">
          <div className="flex items-baseline justify-between gap-2">
            <h4 className="text-sm font-semibold text-[#171717] font-sans">
              {title}
            </h4>
            {timestamp && (
              <span className="text-xs text-[#737373] tabular-nums font-mono shrink-0">
                {timestamp}
              </span>
            )}
          </div>

          {description && (
            <div className="text-xs text-[#525252] mt-1 leading-relaxed font-sans">
              {description}
            </div>
          )}

          {action && (
            <div className="mt-3 flex items-center gap-2">
              {action}
            </div>
          )}
        </div>

        {onDismiss && (
          <button
            onClick={onDismiss}
            className="shrink-0 text-[#737373] hover:text-[#171717] p-1 transition-colors rounded-[4px] hover:bg-[#E5E5E5]"
            aria-label="Dismiss alert"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>
    </div>
  );
};
