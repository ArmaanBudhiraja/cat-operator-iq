import React, { useEffect } from 'react';
import { X } from 'lucide-react';

interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  width?: string;
}

export const Drawer: React.FC<DrawerProps> = ({
  isOpen,
  onClose,
  title,
  subtitle,
  children,
  width = 'max-w-[460px]'
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden select-none">
      {/* Backdrop */}
      <div
        onClick={onClose}
        className="absolute inset-0 bg-[#000000]/30 transition-opacity duration-150"
      />

      {/* Drawer Container */}
      <div className="fixed inset-y-0 right-0 flex max-w-full pl-6">
        <div
          className={`w-screen ${width} bg-[#FFFFFF] border-l border-[#E5E5E5] shadow-[-4px_0_24px_rgba(0,0,0,0.12)] flex flex-col justify-between transform transition-transform duration-150 ease-out`}
        >
          {/* Header */}
          <div className="px-5 py-4 border-b border-[#E5E5E5] flex items-start justify-between bg-[#FAFAFA]">
            <div>
              <h3 className="text-base font-semibold text-[#171717] font-sans">
                {title}
              </h3>
              {subtitle && (
                <p className="text-xs text-[#737373] mt-0.5 font-sans">
                  {subtitle}
                </p>
              )}
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-[4px] text-[#737373] hover:text-[#171717] hover:bg-[#E5E5E5] transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Body */}
          <div className="flex-1 overflow-y-auto p-5 space-y-5 bg-[#FFFFFF]">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};
