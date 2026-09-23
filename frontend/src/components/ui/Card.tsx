import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  variant?: 'default' | 'elevated' | 'interactive' | 'critical' | 'warning';
  noPadding?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  noPadding = false,
  className = '',
  ...props
}) => {
  const variantStyles = {
    default: 'bg-[#FFFFFF] border-[#E5E5E5] shadow-[0_1px_2px_rgba(0,0,0,0.04)]',
    elevated: 'bg-[#FAFAFA] border-[#E5E5E5]',
    interactive: 'bg-[#FFFFFF] border-[#E5E5E5] hover:border-[#737373] hover:bg-[#FAFAFA] transition-colors cursor-pointer shadow-[0_1px_2px_rgba(0,0,0,0.04)]',
    critical: 'bg-[#FFFFFF] border-2 border-[#111111] shadow-[0_1px_4px_rgba(0,0,0,0.08)]',
    warning: 'bg-[#FFFFFF] border border-[#737373]',
  }[variant];

  return (
    <div
      className={`border rounded-[6px] ${variantStyles} ${noPadding ? '' : 'p-4 sm:p-5'} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<{
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  badge?: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}> = ({ title, subtitle, badge, action, className = '' }) => (
  <div className={`flex items-start justify-between gap-3 mb-3 pb-2.5 border-b border-[#E5E5E5] ${className}`}>
    <div className="min-w-0">
      <div className="flex items-center gap-2">
        <h3 className="text-sm font-semibold text-[#171717] font-sans">
          {title}
        </h3>
        {badge}
      </div>
      {subtitle && (
        <p className="text-xs text-[#737373] mt-0.5 leading-relaxed font-sans">
          {subtitle}
        </p>
      )}
    </div>
    {action && <div className="flex-shrink-0 flex items-center gap-2">{action}</div>}
  </div>
);
