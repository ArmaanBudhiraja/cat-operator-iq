import React from 'react';
import { RadarWorker } from '../types';
import { Badge } from './ui/Badge';

interface ProximityRadarProps {
  workers: RadarWorker[];
  machineId?: string;
  isSimulated?: boolean;
}

export const ProximityRadar: React.FC<ProximityRadarProps> = ({
  workers = [],
  machineId = 'EXC001',
}) => {
  const center = 160;
  const maxRadius = 140; // ~14 meters
  const scale = maxRadius / 14; // 10 px per meter

  const criticalRadius = 3.0 * scale; // 30px
  const warningRadius = 6.0 * scale; // 60px
  const safeRadius = 12.0 * scale; // 120px

  const hasCritical = workers.some((w) => w.distance <= 3.0);
  const hasWarning = workers.some((w) => w.distance > 3.0 && w.distance <= 6.0);

  const radarStatus = hasCritical ? 'critical' : hasWarning ? 'warning' : 'safe';

  return (
    <div className="border border-[#E5E5E5] rounded-[6px] bg-[#FFFFFF] p-5 shadow-xs">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4 pb-3 border-b border-[#E5E5E5]">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-semibold text-[#171717] font-sans">
              Proximity perimeter
            </h3>
            <Badge variant={radarStatus} size="sm">
              {hasCritical ? 'Critical breach' : hasWarning ? 'Attention' : 'Normal'}
            </Badge>
          </div>
          <p className="text-xs text-[#737373] mt-0.5 font-sans">
            LiDAR and ultrasonic perimeter sensor tracking · {machineId}
          </p>
        </div>

        <div className="flex items-center gap-4 text-xs font-sans text-[#737373]">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-[#111111]"></span>
            <span>&lt;3m Critical</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-[#737373]"></span>
            <span>3–6m Attention</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-[#D4D4D4]"></span>
            <span>6–12m Normal</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Radar Viewport */}
        <div className="lg:col-span-7 flex justify-center py-1">
          <div className="relative w-[300px] h-[300px] bg-[#FAFAFA] rounded-full border border-[#E5E5E5] p-2">
            <svg viewBox="0 0 320 320" className="w-full h-full">
              {/* Outer boundary */}
              <circle
                cx={center}
                cy={center}
                r={maxRadius}
                fill="none"
                stroke="#E5E5E5"
                strokeWidth="1"
              />

              {/* Safe Zone (6m to 12m) */}
              <circle
                cx={center}
                cy={center}
                r={safeRadius}
                fill="none"
                stroke="#D4D4D4"
                strokeWidth="1"
                strokeDasharray="3 3"
              />

              {/* Warning Zone (3m to 6m) */}
              <circle
                cx={center}
                cy={center}
                r={warningRadius}
                fill="none"
                stroke="#737373"
                strokeWidth="1"
              />

              {/* Critical Danger Zone (0 to 3m) */}
              <circle
                cx={center}
                cy={center}
                r={criticalRadius}
                fill={hasCritical ? 'rgba(0, 0, 0, 0.04)' : 'none'}
                stroke="#171717"
                strokeWidth="1.5"
              />

              {/* Subtle Crosshairs */}
              <line
                x1={center}
                y1={20}
                x2={center}
                y2={300}
                stroke="#E5E5E5"
                strokeWidth="1"
              />
              <line
                x1={20}
                y1={center}
                x2={300}
                y2={center}
                stroke="#E5E5E5"
                strokeWidth="1"
              />

              {/* Range Markers */}
              <text x={center + 5} y={center - criticalRadius + 10} fill="#737373" fontSize="9" fontFamily="sans-serif">
                3m
              </text>
              <text x={center + 5} y={center - warningRadius + 10} fill="#737373" fontSize="9" fontFamily="sans-serif">
                6m
              </text>
              <text x={center + 5} y={center - safeRadius + 10} fill="#737373" fontSize="9" fontFamily="sans-serif">
                12m
              </text>

              {/* Central Machine Marker */}
              <g transform={`translate(${center - 14}, ${center - 14})`}>
                <rect
                  width="28"
                  height="28"
                  rx="4"
                  fill="#FFFFFF"
                  stroke="#171717"
                  strokeWidth="1.5"
                />
                <text
                  x="14"
                  y="18"
                  textAnchor="middle"
                  fill="#171717"
                  fontSize="9"
                  fontFamily="sans-serif"
                  fontWeight="bold"
                >
                  CAT
                </text>
              </g>

              {/* Detected Personnel Markers */}
              {workers.map((w) => {
                const px = center + w.x * scale;
                const py = center - w.y * scale;
                const isCrit = w.distance <= 3.0;

                return (
                  <g key={w.id} className="transition-all duration-300">
                    {/* Ring highlight if critical */}
                    {isCrit && (
                      <circle
                        cx={px}
                        cy={py}
                        r="9"
                        fill="none"
                        stroke="#111111"
                        strokeWidth="1.5"
                        strokeDasharray="2 2"
                      />
                    )}

                    {/* Marker Dot */}
                    <circle
                      cx={px}
                      cy={py}
                      r="4"
                      fill="#111111"
                      stroke="#FFFFFF"
                      strokeWidth="1.5"
                    />

                    {/* Distance badge */}
                    <rect
                      x={px + 7}
                      y={py - 8}
                      width="40"
                      height="15"
                      rx="3"
                      fill="#FFFFFF"
                      stroke="#D4D4D4"
                      strokeWidth="1"
                    />
                    <text
                      x={px + 27}
                      y={py + 3}
                      textAnchor="middle"
                      fill="#171717"
                      fontSize="9"
                      fontFamily="monospace"
                      fontWeight="500"
                    >
                      {w.distance.toFixed(1)}m
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>
        </div>

        {/* Personnel List */}
        <div className="lg:col-span-5 space-y-2">
          <div className="flex items-center justify-between text-xs text-[#525252] font-medium pb-2 border-b border-[#E5E5E5]">
            <span>Personnel ({workers.length})</span>
            <span>Distance</span>
          </div>

          {workers.length === 0 ? (
            <div className="py-6 text-center text-xs text-[#737373] font-sans">
              No ground personnel detected in perimeter.
            </div>
          ) : (
            <div className="space-y-1.5">
              {workers.map((w) => {
                const isCrit = w.distance <= 3.0;
                const isWarn = w.distance > 3.0 && w.distance <= 6.0;
                const badgeVariant = isCrit ? 'critical' : isWarn ? 'warning' : 'safe';

                return (
                  <div
                    key={w.id}
                    className={`flex items-center justify-between p-2.5 rounded-[4px] border transition-colors ${
                      isCrit
                        ? 'border-[#111111] bg-[#FAFAFA]'
                        : isWarn
                        ? 'border-[#737373] bg-[#FFFFFF]'
                        : 'border-[#E5E5E5] bg-[#FFFFFF]'
                    }`}
                  >
                    <div>
                      <div className="text-xs font-semibold text-[#171717] font-sans">
                        {w.name}
                      </div>
                      <div className="text-xs text-[#737373] font-sans">
                        Angle {w.angle.toFixed(0)}° · {w.status}
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="text-xs font-mono font-bold text-[#171717] tabular-nums">
                        {w.distance.toFixed(1)} m
                      </div>
                      <Badge variant={badgeVariant} size="sm">
                        {isCrit ? 'Critical' : isWarn ? 'Attention' : 'Normal'}
                      </Badge>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
