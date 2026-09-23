import React from 'react';

interface SectionHeaderProps {
  title: string;
  count?: number | string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

export const SectionHeader: React.FC<SectionHeaderProps> = ({
  title,
  count,
  description,
  action,
  className = '',
}) => {
  return (
    <div className={`flex flex-wrap items-center justify-between gap-3 mb-3 ${className}`}>
      <div>
        <div className="flex items-center gap-2">
          <h2 className="text-base font-semibold text-[#171717] font-sans">
            {title}
          </h2>
          {count !== undefined && (
            <span className="text-xs px-2 py-0.5 rounded-[4px] bg-[#FAFAFA] border border-[#E5E5E5] text-[#525252] font-mono tabular-nums">
              {count}
            </span>
          )}
        </div>
        {description && (
          <p className="text-xs text-[#737373] mt-0.5 font-sans leading-relaxed">{description}</p>
        )}
      </div>
      {action && <div className="flex items-center gap-2">{action}</div>}
    </div>
  );
};
