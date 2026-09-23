import React, { createContext, useContext, useEffect, useState } from 'react';
import { LiveTelemetryState } from '../types';
import { api } from '../services/api';

interface SimulationContextType {
  liveState: LiveTelemetryState | null;
  isConnected: boolean;
  injectHazard: (hazardType: string) => Promise<void>;
  resetSimulation: () => Promise<void>;
  refreshLive: () => Promise<void>;
}

const SimulationContext = createContext<SimulationContextType | undefined>(undefined);

export const SimulationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [liveState, setLiveState] = useState<LiveTelemetryState | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const fetchState = async () => {
    try {
      const state = await api.getLiveSafety();
      setLiveState(state);
      setIsConnected(true);
    } catch (e) {
      console.error('Polling error:', e);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchState();

    // Setup WebSocket with fallback to polling
    let ws: WebSocket | null = null;
    let pollInterval: any = null;

    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/ws/telemetry`;
      ws = new WebSocket(wsUrl);

      ws.onopen = () => {
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setLiveState(data);
        } catch (err) {
          console.error('WS parse error:', err);
        }
      };

      ws.onerror = () => {
        setIsConnected(false);
      };

      ws.onclose = () => {
        setIsConnected(false);
        // Fallback polling if WS closes
        if (!pollInterval) {
          pollInterval = setInterval(fetchState, 2000);
        }
      };
    } catch (err) {
      // WS failed to construct, fallback to polling
      pollInterval = setInterval(fetchState, 2000);
    }

    return () => {
      if (ws) ws.close();
      if (pollInterval) clearInterval(pollInterval);
    };
  }, []);

  const injectHazard = async (hazardType: string) => {
    await api.injectHazard(hazardType);
    await fetchState();
  };

  const resetSimulation = async () => {
    await api.resetSimulation();
    await fetchState();
  };

  return (
    <SimulationContext.Provider
      value={{
        liveState,
        isConnected,
        injectHazard,
        resetSimulation,
        refreshLive: fetchState
      }}
    >
      {children}
    </SimulationContext.Provider>
  );
};

export const useSimulation = () => {
  const ctx = useContext(SimulationContext);
  if (!ctx) throw new Error('useSimulation must be used within SimulationProvider');
  return ctx;
};
