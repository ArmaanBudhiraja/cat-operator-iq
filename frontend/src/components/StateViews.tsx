import React from 'react';
import { AlertCircle, RefreshCw, Shield } from 'lucide-react';
import { Button } from './ui/Button';

export const SkeletonCard: React.FC<{ rows?: number; className?: string }> = ({ rows = 3, className = '' }) => (
  <div className={`bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-4 space-y-3 ${className}`}>
    <div className="flex justify-between items-center">
      <div className="h-3 bg-[#F0F0F0] rounded w-1/4 animate-pulse"></div>
      <div className="h-3 bg-[#F0F0F0] rounded w-12 animate-pulse"></div>
    </div>
    <div className="h-6 bg-[#F0F0F0] rounded w-1/3 my-2 animate-pulse"></div>
    {Array.from({ length: rows }).map((_, i) => (
      <div key={i} className="h-2.5 bg-[#F0F0F0] rounded w-full animate-pulse"></div>
    ))}
  </div>
);

export const EmptyState: React.FC<{
  title?: string;
  message?: string;
  icon?: React.ReactNode;
  actionLabel?: string;
  onAction?: () => void;
  quiet?: boolean;
}> = ({
  title = 'Everything is quiet',
  message = 'No active incidents or alerts requiring intervention at this time.',
  icon,
  actionLabel,
  onAction,
}) => (
  <div className="border border-[#E5E5E5] rounded-[6px] bg-[#FFFFFF] p-8 text-center flex flex-col items-center justify-center my-4 shadow-xs">
    <div className="w-9 h-9 rounded-full bg-[#FAFAFA] border border-[#E5E5E5] flex items-center justify-center text-[#737373] mb-3">
      {icon ? (
        icon
      ) : (
        <Shield className="w-4 h-4 text-[#737373]" />
      )}
    </div>
    <h4 className="text-sm font-semibold text-[#171717] font-sans">
      {title}
    </h4>
    <p className="text-xs text-[#525252] max-w-sm mt-1 mb-4 leading-relaxed font-sans">
      {message}
    </p>
    {actionLabel && onAction && (
      <Button variant="secondary" size="sm" onClick={onAction}>
        {actionLabel}
      </Button>
    )}
  </div>
);

export const ErrorState: React.FC<{
  title?: string;
  error?: string;
  lastUpdated?: string;
  onRetry?: () => void;
}> = ({
  title = 'Telemetry unavailable',
  error,
  lastUpdated = '2 minutes ago',
  onRetry,
}) => (
  <div className="border border-[#D4D4D4] bg-[#FFFFFF] rounded-[6px] p-6 text-center my-4 flex flex-col items-center shadow-xs">
    <div className="w-9 h-9 rounded-full bg-[#FAFAFA] border border-[#E5E5E5] flex items-center justify-center text-[#171717] mb-3">
      <AlertCircle className="w-4 h-4 text-[#171717]" />
    </div>
    <h4 className="text-sm font-semibold text-[#171717] font-sans">
      {title}
    </h4>
    <p className="text-xs text-[#525252] mt-1 mb-1 font-sans">
      The latest machine data could not be retrieved.
    </p>
    <p className="text-xs text-[#737373] font-sans mb-3">
      Last successful update: {lastUpdated}
    </p>
    {error && (
      <p className="text-xs text-[#737373] max-w-md font-mono bg-[#FAFAFA] px-2.5 py-1 rounded border border-[#E5E5E5] mb-4">
        {error.length > 90 ? `${error.slice(0, 90)}...` : error}
      </p>
    )}
    {onRetry && (
      <Button variant="secondary" size="sm" onClick={onRetry} icon={<RefreshCw className="w-3.5 h-3.5" />}>
        Retry connection
      </Button>
    )}
  </div>
);

export const PageHeader: React.FC<{
  title: string;
  subtitle?: string;
  badge?: React.ReactNode;
  action?: React.ReactNode;
}> = ({ title, subtitle, badge, action }) => (
  <div className="flex flex-wrap items-center justify-between gap-4 mb-5 pb-3 border-b border-[#E5E5E5]">
    <div>
      <div className="flex items-center gap-3">
        <h1 className="text-2xl font-semibold text-[#171717] tracking-tight font-sans">
          {title}
        </h1>
        {badge}
      </div>
      {subtitle && <p className="text-xs text-[#737373] mt-0.5 font-sans">{subtitle}</p>}
    </div>
    {action && <div className="flex items-center gap-2">{action}</div>}
  </div>
);
