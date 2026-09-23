import React from 'react';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

interface KpiCardProps {
  label: string;
  value: string | number;
  unit?: string;
  subtext?: string;
  delta?: string;
  deltaPositive?: boolean;
  icon?: React.ComponentType<{ className?: string }>;
  accentColor?: 'yellow' | 'green' | 'amber' | 'red';
  className?: string;
}

export const KpiCard: React.FC<KpiCardProps> = ({
  label,
  value,
  unit,
  subtext,
  delta,
  deltaPositive,
  icon: Icon,
  className = '',
}) => {
  return (
    <div className={`bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-3.5 transition-colors hover:border-[#D4D4D4] shadow-[0_1px_2px_rgba(0,0,0,0.03)] ${className}`}>
      <div className="flex items-center justify-between gap-2 mb-1">
        <span className="text-xs font-sans text-[#525252] font-medium">
          {label}
        </span>
        {Icon && (
          <div className="text-[#737373]">
            <Icon className="w-3.5 h-3.5" />
          </div>
        )}
      </div>

      <div className="flex items-baseline gap-1.5 my-0.5">
        <span className="text-2xl font-semibold font-sans tracking-tight text-[#171717] tabular-nums">
          {value}
        </span>
        {unit && <span className="text-xs font-sans text-[#737373]">{unit}</span>}
      </div>

      {(subtext || delta) && (
        <div className="mt-2 pt-2 border-t border-[#E5E5E5] flex items-center justify-between text-xs font-sans">
          {subtext && <span className="text-[#737373] truncate">{subtext}</span>}
          {delta && (
            <span className="flex items-center gap-0.5 ml-auto font-medium text-[#171717] tabular-nums">
              {deltaPositive ? (
                <ArrowUpRight className="w-3 h-3 text-[#525252]" />
              ) : (
                <ArrowDownRight className="w-3 h-3 text-[#171717]" />
              )}
              {delta}
            </span>
          )}
        </div>
      )}
    </div>
  );
};
