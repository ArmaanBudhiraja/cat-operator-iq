import React from 'react';
import { TelemetryData } from '../types';
import { Badge } from './ui/Badge';
import { ProgressBar } from './ui/ProgressBar';

interface TelemetryLiveFeedProps {
  telemetry: TelemetryData;
}

export const TelemetryLiveFeed: React.FC<TelemetryLiveFeedProps> = ({ telemetry }) => {
  const isSeatbeltUnfastened = telemetry.seatbelt_status.toLowerCase() === 'unfastened';
  const isOverheating = telemetry.engine_temperature >= 100.0;
  const isVibHigh = telemetry.vibration >= 3.0;

  return (
    <div className="bg-[#FFFFFF] border border-[#E5E5E5] rounded-[6px] p-5 shadow-xs font-sans">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4 pb-3 border-b border-[#E5E5E5]">
        <div>
          <div className="flex items-center gap-2.5">
            <h3 className="text-sm font-semibold text-[#171717] font-sans">
              Sensor telemetry stream
            </h3>
            <Badge variant="safe" size="sm">
              Live CAN-bus
            </Badge>
          </div>
          <p className="text-xs text-[#737373] mt-0.5 font-sans">
            Real-time mechanical sensor feed · Machine: {telemetry.machine_id}
          </p>
        </div>

        <div className="text-xs text-[#737373] font-sans">
          Packet: <span className="text-[#171717] tabular-nums font-mono font-medium">{telemetry.timestamp.split('T')[1]?.slice(0, 8) || telemetry.timestamp.slice(11, 19)}</span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3 text-xs">
        {/* Engine RPM */}
        <div className="p-3.5 bg-[#FAFAFA] rounded-[4px] border border-[#E5E5E5]">
          <span className="text-xs text-[#525252] font-medium block">Engine RPM</span>
          <div className="text-xl font-semibold text-[#171717] mt-1 tabular-nums font-sans">
            {telemetry.engine_rpm.toFixed(0)}
          </div>
          <div className="mt-2">
            <ProgressBar value={telemetry.engine_rpm} max={2200} size="xs" />
          </div>
        </div>

        {/* Engine Temp */}
        <div className={`p-3.5 rounded-[4px] border transition-colors ${
          isOverheating ? 'bg-[#FFFFFF] border-2 border-[#111111]' : 'bg-[#FAFAFA] border-[#E5E5E5]'
        }`}>
          <span className="text-xs text-[#525252] font-medium block">Engine temp</span>
          <div className="text-xl font-semibold text-[#171717] mt-1 tabular-nums font-sans">
            {telemetry.engine_temperature.toFixed(1)} <span className="text-xs font-normal text-[#737373]">°C</span>
          </div>
          <div className="text-xs text-[#737373] mt-1.5 font-sans">
            Coolant: {telemetry.coolant_temperature.toFixed(0)}°C
          </div>
        </div>

        {/* Vibration */}
        <div className={`p-3.5 rounded-[4px] border transition-colors ${
          isVibHigh ? 'bg-[#FFFFFF] border border-[#171717]' : 'bg-[#FAFAFA] border-[#E5E5E5]'
        }`}>
          <span className="text-xs text-[#525252] font-medium block">Vibration</span>
          <div className="text-xl font-semibold text-[#171717] mt-1 tabular-nums font-sans">
            {telemetry.vibration.toFixed(2)} <span className="text-xs font-normal text-[#737373]">mm/s</span>
          </div>
          <div className="text-xs text-[#737373] mt-1.5 font-sans">
            {isVibHigh ? '↑ Elevated' : 'Baseline 1.75'}
          </div>
        </div>

        {/* Oil Pressure */}
        <div className="p-3.5 bg-[#FAFAFA] rounded-[4px] border border-[#E5E5E5]">
          <span className="text-xs text-[#525252] font-medium block">Oil pressure</span>
          <div className="text-xl font-semibold text-[#171717] mt-1 tabular-nums font-sans">
            {telemetry.oil_pressure.toFixed(1)} <span className="text-xs font-normal text-[#737373]">psi</span>
          </div>
          <div className="text-xs text-[#737373] mt-1.5 font-sans">
            Hydraulic: {telemetry.hydraulic_pressure.toFixed(0)} bar
          </div>
        </div>

        {/* Idle Time */}
        <div className="p-3.5 bg-[#FAFAFA] rounded-[4px] border border-[#E5E5E5]">
          <span className="text-xs text-[#525252] font-medium block">Idle time</span>
          <div className="text-xl font-semibold text-[#171717] mt-1 tabular-nums font-sans">
            {telemetry.idling_time_min.toFixed(0)} <span className="text-xs font-normal text-[#737373]">min</span>
          </div>
          <div className="text-xs text-[#737373] mt-1.5 font-sans">
            Fuel: {telemetry.fuel_used_l.toFixed(1)} L
          </div>
        </div>

        {/* Seatbelt Status */}
        <div className={`p-3.5 rounded-[4px] border flex flex-col justify-between transition-colors ${
          isSeatbeltUnfastened ? 'bg-[#FFFFFF] border-2 border-[#111111]' : 'bg-[#FAFAFA] border-[#E5E5E5]'
        }`}>
          <span className="text-xs text-[#525252] font-medium block">Seatbelt</span>
          <div className="my-1">
            <Badge variant={isSeatbeltUnfastened ? 'critical' : 'safe'} size="sm">
              {telemetry.seatbelt_status}
            </Badge>
          </div>
          <div className="text-xs text-[#737373] font-sans">
            {isSeatbeltUnfastened ? 'Interlock alert' : 'Compliant'}
          </div>
        </div>
      </div>
    </div>
  );
};
