import React from 'react';
import { useLocation } from 'react-router-dom';
import { useRole } from '../context/RoleContext';
import { useSimulation } from '../context/SimulationContext';
import { ChevronDown, HardHat, Users } from 'lucide-react';

const routeContextMap: Record<string, { title: string; subtitle: string }> = {
  '/dashboard': {
    title: 'Dashboard',
    subtitle: 'Morning shift · EXC001'
  },
  '/tasks': {
    title: 'Tasks',
    subtitle: 'Operational queue · EXC001'
  },
  '/machines': {
    title: 'Machines',
    subtitle: 'Fleet & diagnostics · EXC001'
  },
  '/safety': {
    title: 'Safety',
    subtitle: 'Perimeter monitoring · EXC001'
  },
  '/behavior': {
    title: 'Behavior',
    subtitle: 'Baseline comparisons · EXC001'
  },
  '/training': {
    title: 'Training',
    subtitle: 'Operator qualifications · OP001'
  },
  '/incidents': {
    title: 'Incidents',
    subtitle: 'Safety audit records · EXC001'
  },
  '/assistant': {
    title: 'AI Assistant',
    subtitle: 'Operational intelligence layer'
  },
  '/reports': {
    title: 'Reports',
    subtitle: 'Shift compliance records'
  }
};

export const Navbar: React.FC = () => {
  const location = useLocation();
  const { role, setRole, activeMachineId, setActiveMachineId } = useRole();
  const { liveState } = useSimulation();

  const currentRouteInfo = routeContextMap[location.pathname] || {
    title: 'OperatorIQ',
    subtitle: 'Operational intelligence'
  };

  const machines = [
    { id: 'EXC001', label: 'EXC001 · CAT 336' },
    { id: 'WHL002', label: 'WHL002 · CAT 950M' },
    { id: 'DOZ003', label: 'DOZ003 · CAT D6 XE' },
    { id: 'GRD004', label: 'GRD004 · CAT 140' },
    { id: 'DMP005', label: 'DMP005 · CAT 730' }
  ];

  return (
    <header className="h-14 bg-[#FFFFFF] border-b border-[#E5E5E5] px-6 flex items-center justify-between gap-4 sticky top-0 z-30 select-none">
      {/* Page Title & Context */}
      <div className="flex items-center gap-3 min-w-0">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h1 className="text-sm font-semibold tracking-tight text-[#171717] font-sans">
              {currentRouteInfo.title}
            </h1>
            <span className="text-xs font-mono text-[#525252] px-2 py-0.5 rounded-[4px] bg-[#FAFAFA] border border-[#E5E5E5]">
              {activeMachineId}
            </span>
          </div>
          <p className="text-xs text-[#737373] hidden sm:block truncate font-sans">
            {currentRouteInfo.subtitle}
          </p>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3 shrink-0">
        {/* Machine Selector */}
        <div className="relative flex items-center bg-[#FFFFFF] border border-[#E5E5E5] hover:border-[#D4D4D4] rounded-[4px] px-2.5 py-1 text-xs transition-colors shadow-xs">
          <select
            value={activeMachineId}
            onChange={(e) => setActiveMachineId(e.target.value)}
            className="bg-transparent text-[#171717] font-mono text-xs font-normal appearance-none pr-5 focus:outline-none cursor-pointer"
          >
            {machines.map((m) => (
              <option key={m.id} value={m.id} className="bg-[#FFFFFF] text-[#171717] font-mono">
                {m.label}
              </option>
            ))}
          </select>
          <ChevronDown className="w-3.5 h-3.5 text-[#737373] absolute right-2 pointer-events-none" />
        </div>

        {/* Live Status Indicator */}
        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-[4px] border border-[#E5E5E5] bg-[#FAFAFA] text-xs font-sans">
          <span className="w-2 h-2 rounded-full bg-[#171717]"></span>
          <span className="text-[#171717] font-medium text-xs">Live</span>
          {liveState && (
            <span className="text-[#737373] text-xs pl-1.5 border-l border-[#E5E5E5] tabular-nums font-mono">
              {liveState.telemetry.engine_rpm.toFixed(0)} RPM
            </span>
          )}
        </div>

        {/* Role Switcher */}
        <div className="flex items-center bg-[#F5F5F5] border border-[#E5E5E5] rounded-[4px] p-0.5 text-xs font-sans">
          <button
            onClick={() => setRole('Operator')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-[3px] text-xs transition-colors ${
              role === 'Operator'
                ? 'bg-[#FFFFFF] text-[#171717] font-medium border border-[#E5E5E5] shadow-xs'
                : 'text-[#737373] hover:text-[#171717]'
            }`}
          >
            <HardHat className="w-3 h-3 text-current" />
            <span className="hidden sm:inline">Operator</span>
          </button>
          <button
            onClick={() => setRole('Supervisor')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-[3px] text-xs transition-colors ${
              role === 'Supervisor'
                ? 'bg-[#FFFFFF] text-[#171717] font-medium border border-[#E5E5E5] shadow-xs'
                : 'text-[#737373] hover:text-[#171717]'
            }`}
          >
            <Users className="w-3 h-3 text-current" />
            <span className="hidden sm:inline">Fleet</span>
          </button>
        </div>
      </div>
    </header>
  );
};
