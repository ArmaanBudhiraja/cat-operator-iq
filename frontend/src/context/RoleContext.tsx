import React, { createContext, useContext, useState } from 'react';
import { UserRole } from '../types';

interface RoleContextType {
  role: UserRole;
  setRole: (role: UserRole) => void;
  activeOperatorId: string;
  setActiveOperatorId: (id: string) => void;
  activeMachineId: string;
  setActiveMachineId: (id: string) => void;
}

const RoleContext = createContext<RoleContextType | undefined>(undefined);

export const RoleProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [role, setRole] = useState<UserRole>('Operator');
  const [activeOperatorId, setActiveOperatorId] = useState('OP001');
  const [activeMachineId, setActiveMachineId] = useState('EXC001');

  return (
    <RoleContext.Provider
      value={{
        role,
        setRole,
        activeOperatorId,
        setActiveOperatorId,
        activeMachineId,
        setActiveMachineId
      }}
    >
      {children}
    </RoleContext.Provider>
  );
};

export const useRole = () => {
  const ctx = useContext(RoleContext);
  if (!ctx) throw new Error('useRole must be used within RoleProvider');
  return ctx;
};
