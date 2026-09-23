import React from 'react';

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  baseline?: string;
  delta?: string;
  status?: 'normal' | 'elevated' | 'warning' | 'positive';
  icon?: React.ReactNode;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  unit,
  baseline,
  delta,
  icon,
  className = ''
}) => {
  return (
    <div
      className={`bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-3.5 transition-colors hover:border-[#D4D4D4] shadow-[0_1px_2px_rgba(0,0,0,0.03)] ${className}`}
    >
      <div className="flex items-center justify-between gap-2 mb-1">
        <span className="text-xs font-sans text-[#525252] font-medium">
          {label}
        </span>
        {icon && <span className="text-[#737373]">{icon}</span>}
      </div>

      <div className="flex items-baseline gap-1.5 my-0.5">
        <span className="text-2xl font-semibold font-sans tracking-tight text-[#171717] tabular-nums">
          {value}
        </span>
        {unit && (
          <span className="text-xs font-sans text-[#737373]">
            {unit}
          </span>
        )}
      </div>

      {(baseline || delta) && (
        <div className="mt-2 pt-2 border-t border-[#E5E5E5] flex items-center justify-between text-xs font-sans">
          {baseline && (
            <span className="text-[#737373] truncate">
              {baseline}
            </span>
          )}
          {delta && (
            <span className="font-semibold text-[#171717] shrink-0 tabular-nums">
              {delta}
            </span>
          )}
        </div>
      )}
    </div>
  );
};
