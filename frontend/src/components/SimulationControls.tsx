import React, { useState } from 'react';
import { useSimulation } from '../context/SimulationContext';
import { Badge } from './ui/Badge';
import { Button } from './ui/Button';
import { RotateCcw, AlertTriangle, Shield, SlidersHorizontal } from 'lucide-react';

export const SimulationControls: React.FC = () => {
  const { injectHazard, resetSimulation } = useSimulation();
  const [activeHazard, setActiveHazard] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const handleInject = async (type: string) => {
    setActiveHazard(type);
    await injectHazard(type);
  };

  const handleReset = async () => {
    setActiveHazard(null);
    await resetSimulation();
  };

  return (
    <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] px-4 py-2.5 transition-all shadow-xs">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <span className="w-2 h-2 rounded-full bg-[#171717]"></span>
          <span className="text-xs font-sans text-[#171717] font-semibold">
            Telemetry simulation
          </span>
          <span className="text-[#737373] text-xs font-sans hidden sm:inline">
            · Real-time CAN-bus emitter
          </span>
          {activeHazard && (
            <Badge variant="warning" size="sm">
              Hazard: {activeHazard.replace('_', ' ')}
            </Badge>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Button
            size="sm"
            variant="ghost"
            onClick={() => setIsExpanded(!isExpanded)}
            icon={<SlidersHorizontal className="w-3.5 h-3.5 text-[#525252]" />}
          >
            {isExpanded ? 'Hide controls' : 'Simulation controls'}
          </Button>
          {activeHazard && (
            <Button
              size="sm"
              variant="secondary"
              onClick={handleReset}
              icon={<RotateCcw className="w-3 h-3 text-[#525252]" />}
            >
              Reset baseline
            </Button>
          )}
        </div>
      </div>

      {isExpanded && (
        <div className="mt-2.5 pt-2.5 border-t border-[#E5E5E5] flex flex-wrap items-center gap-2 text-xs font-sans">
          <span className="text-xs text-[#737373] mr-1">
            Inject scenario:
          </span>
          <Button
            size="sm"
            variant={activeHazard === 'worker_proximity' ? 'primary' : 'secondary'}
            onClick={() => handleInject('worker_proximity')}
            icon={<Shield className="w-3 h-3" />}
          >
            Worker incursion (2.1m)
          </Button>

          <Button
            size="sm"
            variant={activeHazard === 'seatbelt_unfastened' ? 'primary' : 'secondary'}
            onClick={() => handleInject('seatbelt_unfastened')}
            icon={<AlertTriangle className="w-3 h-3" />}
          >
            Unfasten seatbelt
          </Button>

          <Button
            size="sm"
            variant={activeHazard === 'vibration_spike' ? 'primary' : 'secondary'}
            onClick={() => handleInject('vibration_spike')}
          >
            Vibration spike (4.2 mm/s)
          </Button>

          <Button
            size="sm"
            variant={activeHazard === 'overheating' ? 'primary' : 'secondary'}
            onClick={() => handleInject('overheating')}
          >
            Thermal runaway (108°C)
          </Button>

          <Button
            size="sm"
            variant="ghost"
            onClick={handleReset}
            icon={<RotateCcw className="w-3 h-3" />}
          >
            Reset
          </Button>
        </div>
      )}
    </div>
  );
};
