import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { RoleProvider } from './context/RoleContext';
import { SimulationProvider } from './context/SimulationContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';

// Pages
import { DashboardPage } from './pages/DashboardPage';
import { TasksPage } from './pages/TasksPage';
import { SafetyPage } from './pages/SafetyPage';
import { MachineHealthPage } from './pages/MachineHealthPage';
import { BehaviorPage } from './pages/BehaviorPage';
import { TrainingPage } from './pages/TrainingPage';
import { IncidentsPage } from './pages/IncidentsPage';
import { AssistantPage } from './pages/AssistantPage';
import { ReportsPage } from './pages/ReportsPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <RoleProvider>
        <SimulationProvider>
          <div className="min-h-screen bg-[#F5F5F5] text-[#171717] flex flex-col font-sans antialiased">
            {/* Top Navigation */}
            <Navbar />

            {/* Main Application Body */}
            <div className="flex-1 flex overflow-hidden">
              {/* Left Navigation Sidebar */}
              <Sidebar />

              {/* Dynamic Content Region */}
              <main className="flex-1 overflow-y-auto p-4 sm:p-6 md:p-8 bg-[#F5F5F5]">
                <Routes>
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/tasks" element={<TasksPage />} />
                  <Route path="/safety" element={<SafetyPage />} />
                  <Route path="/machines" element={<MachineHealthPage />} />
                  <Route path="/behavior" element={<BehaviorPage />} />
                  <Route path="/training" element={<TrainingPage />} />
                  <Route path="/incidents" element={<IncidentsPage />} />
                  <Route path="/assistant" element={<AssistantPage />} />
                  <Route path="/reports" element={<ReportsPage />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </main>
            </div>
          </div>
        </SimulationProvider>
      </RoleProvider>
    </BrowserRouter>
  );
};

export default App;
