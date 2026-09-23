import React from 'react';
import { NavLink } from 'react-router-dom';
import { useRole } from '../context/RoleContext';
import {
  LayoutDashboard, CheckSquare, Activity, Shield,
  BrainCircuit, FileText, GraduationCap, AlertTriangle,
  Bot
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const { role, activeMachineId } = useRole();

  const sections = [
    {
      title: 'Overview',
      items: [
        { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard }
      ]
    },
    {
      title: 'Operations',
      items: [
        { to: '/tasks', label: role === 'Operator' ? 'Tasks' : 'Task Dispatch', icon: CheckSquare },
        { to: '/machines', label: role === 'Operator' ? 'Machines' : 'Fleet Overview', icon: Activity },
        { to: '/safety', label: 'Safety', icon: Shield }
      ]
    },
    {
      title: 'Insights',
      items: [
        { to: '/behavior', label: 'Behavior', icon: BrainCircuit },
        { to: '/reports', label: 'Reports', icon: FileText }
      ]
    },
    {
      title: 'People',
      items: [
        { to: '/training', label: 'Training', icon: GraduationCap }
      ]
    },
    {
      title: 'System',
      items: [
        { to: '/incidents', label: 'Incidents', icon: AlertTriangle },
        { to: '/assistant', label: 'AI Assistant', icon: Bot }
      ]
    }
  ];

  return (
    <aside className="w-[230px] bg-[#111111] border-r border-[#262626] flex flex-col justify-between p-3.5 shrink-0 select-none">
      <div>
        {/* Wordmark */}
        <div className="px-3 py-2.5 mb-3 border-b border-[#262626] flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="bg-[#FFFFFF] text-[#000000] font-black text-[11px] px-1.5 py-0.5 rounded-[3px] font-sans tracking-tight">
              CAT
            </span>
            <span className="font-semibold text-sm tracking-tight text-[#FFFFFF] font-sans">
              OperatorIQ
            </span>
          </div>
          <span className="text-[11px] font-sans text-[#737373]">
            {role === 'Operator' ? 'Cab' : 'Fleet'}
          </span>
        </div>

        {/* Navigation Sections */}
        <div className="space-y-3.5">
          {sections.map((sec, sIdx) => (
            <div key={sIdx} className="space-y-0.5">
              <div className="px-3 text-xs font-sans text-[#737373] font-medium mb-1">
                {sec.title}
              </div>

              {sec.items.map((item) => {
                const Icon = item.icon;
                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    className={({ isActive }) =>
                      `flex items-center gap-2.5 px-3 py-2 h-[36px] rounded-[4px] text-xs transition-colors duration-100 ${
                        isActive
                          ? 'bg-[#222222] text-[#FFFFFF] font-medium'
                          : 'text-[#A3A3A3] hover:text-[#FFFFFF] hover:bg-[#1A1A1A]'
                      }`
                    }
                  >
                    <Icon className="w-4 h-4 shrink-0 text-[#737373]" />
                    <span className="font-sans text-[13px]">{item.label}</span>
                  </NavLink>
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Identity & Status */}
      <div className="pt-3 border-t border-[#262626] px-2.5 space-y-1 text-xs">
        <div className="flex items-center justify-between text-[#FFFFFF]">
          <span className="font-semibold font-mono">{activeMachineId}</span>
          <span className="text-xs text-[#737373]">CAT 336</span>
        </div>
        <div className="text-[#A3A3A3] truncate text-xs font-sans">
          {role === 'Operator' ? 'Marcus Vance (OP001)' : 'Fleet Supervisor'}
        </div>
        <div className="flex items-center gap-1.5 text-[#A3A3A3] text-xs pt-1">
          <span className="w-1.5 h-1.5 rounded-full bg-[#FFFFFF]"></span>
          <span>System online</span>
        </div>
      </div>
    </aside>
  );
};
