import React from 'react';
import { Loader2 } from 'lucide-react';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  icon?: React.ReactNode;
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'secondary',
  size = 'md',
  icon,
  loading = false,
  children,
  className = '',
  disabled,
  ...props
}) => {
  const variantStyles: Record<ButtonVariant, string> = {
    primary: 'bg-[#111111] text-[#FFFFFF] font-medium border border-[#111111] hover:bg-[#262626] shadow-sm',
    secondary: 'bg-[#FFFFFF] text-[#171717] border border-[#E5E5E5] hover:bg-[#F5F5F5] hover:border-[#D4D4D4]',
    ghost: 'bg-transparent text-[#525252] border-0 hover:text-[#171717] hover:bg-[#F5F5F5]',
    danger: 'bg-[#FFFFFF] text-[#171717] border border-[#171717] font-medium hover:bg-[#F5F5F5]',
  };

  const sizeStyles: Record<ButtonSize, string> = {
    sm: 'px-2.5 py-1 text-xs rounded-[4px] gap-1.5',
    md: 'px-3 py-1.5 text-xs rounded-[6px] gap-1.5',
    lg: 'px-4 py-2 text-sm rounded-[6px] gap-2 font-medium',
  };

  return (
    <button
      disabled={disabled || loading}
      className={`inline-flex items-center justify-center transition-colors duration-150 select-none disabled:opacity-40 disabled:cursor-not-allowed ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      {...props}
    >
      {loading ? (
        <Loader2 className="w-3.5 h-3.5 animate-spin text-current" />
      ) : (
        icon && <span className="shrink-0">{icon}</span>
      )}
      {children}
    </button>
  );
};
