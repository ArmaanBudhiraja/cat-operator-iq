import React from 'react';

interface ProgressBarProps {
  value: number; // 0 to 100
  max?: number;
  label?: string;
  sublabel?: string;
  variant?: 'white' | 'grey' | 'yellow' | 'safe' | 'warning' | 'critical' | 'neutral';
  size?: 'xs' | 'sm' | 'md';
  showPercent?: boolean;
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  label,
  sublabel,
  size = 'xs',
  showPercent = false,
  className = '',
}) => {
  const percentage = Math.min(Math.max(0, (value / max) * 100), 100);

  const heightClass = {
    xs: 'h-[3px]',
    sm: 'h-[4px]',
    md: 'h-[6px]',
  }[size];

  return (
    <div className={`w-full ${className}`}>
      {(label || showPercent || sublabel) && (
        <div className="flex items-center justify-between text-xs mb-1.5 font-sans">
          <div className="flex items-center gap-2">
            {label && <span className="text-[#171717] text-xs font-medium">{label}</span>}
            {sublabel && <span className="text-[#737373] text-xs">{sublabel}</span>}
          </div>
          {showPercent && (
            <span className="text-[#171717] text-xs font-semibold tabular-nums">{Math.round(percentage)}%</span>
          )}
        </div>
      )}
      <div className={`w-full bg-[#E5E5E5] rounded-[2px] overflow-hidden ${heightClass}`}>
        <div
          className={`${heightClass} bg-[#111111] transition-all duration-150 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
