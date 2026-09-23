import React from 'react';

export type BadgeVariant = 'safe' | 'warning' | 'high' | 'critical' | 'neutral' | 'normal' | 'attention';

interface BadgeProps {
  variant?: BadgeVariant;
  children: React.ReactNode;
  size?: 'sm' | 'md';
  dot?: boolean;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  variant = 'neutral',
  children,
  size = 'sm',
  dot = false,
  className = '',
}) => {
  // Normalize variants
  const normalizedVariant = variant === 'normal' ? 'safe' : variant === 'attention' ? 'warning' : variant;

  const variantStyles: Record<string, string> = {
    safe: 'border-[#E5E5E5] text-[#525252] bg-[#FAFAFA]',
    warning: 'border-[#737373] text-[#171717] bg-[#FFFFFF] font-medium',
    high: 'border-[#171717] text-[#171717] bg-[#F5F5F5] font-semibold',
    critical: 'border-[#000000] text-[#FFFFFF] bg-[#111111] font-semibold shadow-xs',
    neutral: 'border-[#E5E5E5] text-[#737373] bg-[#FAFAFA]',
  };

  const symbolMap: Record<string, string> = {
    safe: '●',
    warning: '△',
    high: '!',
    critical: '◆',
    neutral: '',
  };

  const sizeStyles = size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-2.5 py-1 text-xs';

  return (
    <span
      className={`inline-flex items-center gap-1 font-sans rounded-[4px] border ${sizeStyles} ${variantStyles[normalizedVariant] || variantStyles.neutral} ${className}`}
    >
      {dot && symbolMap[normalizedVariant] && (
        <span className="text-[10px] opacity-90">{symbolMap[normalizedVariant]}</span>
      )}
      <span>{children}</span>
    </span>
  );
};

interface StatusDotProps {
  status: 'safe' | 'warning' | 'high' | 'critical' | 'neutral' | 'live';
  label?: string;
  pulse?: boolean;
}

export const StatusDot: React.FC<StatusDotProps> = ({ status, label, pulse = false }) => {
  const dotClass = {
    safe: 'bg-[#737373]',
    warning: 'bg-[#525252]',
    high: 'bg-[#171717]',
    critical: 'bg-[#000000]',
    neutral: 'bg-[#A3A3A3]',
    live: 'bg-[#171717]',
  }[status];

  return (
    <div className="inline-flex items-center gap-1.5 text-xs font-sans">
      <span className="relative flex h-2 w-2">
        {pulse && (
          <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-30 ${dotClass}`}></span>
        )}
        <span className={`relative inline-flex rounded-full h-2 w-2 ${dotClass}`}></span>
      </span>
      {label && <span className="text-[#525252] text-xs">{label}</span>}
    </div>
  );
};
