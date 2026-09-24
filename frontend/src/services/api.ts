import {
  DashboardData, TaskItem, MachineItem, OperatorItem,
  LiveTelemetryState, IncidentItem, AnomalyItem, TrainingCourse,
  AssistantStatus, AssistantQueryResponse
} from '../types';

const API_BASE = '/api';

export const api = {
  // Dashboard
  async getDashboard(operatorId = 'OP001', machineId = 'EXC001'): Promise<DashboardData> {
    const res = await fetch(`${API_BASE}/dashboard?operator_id=${operatorId}&machine_id=${machineId}`);
    if (!res.ok) throw new Error('Failed to load dashboard');
    return res.json();
  },

  // Tasks
  async getTasks(status?: string, operatorId?: string): Promise<TaskItem[]> {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (operatorId) params.append('operator_id', operatorId);
    const res = await fetch(`${API_BASE}/tasks?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to load tasks');
    return res.json();
  },

  async getTaskDetail(taskId: string): Promise<TaskItem> {
    const res = await fetch(`${API_BASE}/tasks/${taskId}`);
    if (!res.ok) throw new Error('Failed to load task details');
    return res.json();
  },

  async updateTaskStatus(taskId: string, status: string, actualTimeMin?: number) {
    const res = await fetch(`${API_BASE}/tasks/${taskId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status, actual_time_min: actualTimeMin })
    });
    if (!res.ok) throw new Error('Failed to update task');
    return res.json();
  },

  // Machines
  async getMachines(): Promise<MachineItem[]> {
    const res = await fetch(`${API_BASE}/machines`);
    if (!res.ok) throw new Error('Failed to load machines');
    return res.json();
  },

  async getMachineDetail(machineId: string): Promise<MachineItem> {
    const res = await fetch(`${API_BASE}/machines/${machineId}`);
    if (!res.ok) throw new Error('Failed to load machine detail');
    return res.json();
  },

  async getMachineTelemetryHistory(machineId: string) {
    const res = await fetch(`${API_BASE}/machines/${machineId}/telemetry`);
    if (!res.ok) throw new Error('Failed to load telemetry history');
    return res.json();
  },

  // Operators
  async getOperators(): Promise<OperatorItem[]> {
    const res = await fetch(`${API_BASE}/operators`);
    if (!res.ok) throw new Error('Failed to load operators');
    return res.json();
  },

  async getOperatorDetail(operatorId: string) {
    const res = await fetch(`${API_BASE}/operators/${operatorId}`);
    if (!res.ok) throw new Error('Failed to load operator detail');
    return res.json();
  },

  // Safety
  async getLiveSafety(): Promise<LiveTelemetryState> {
    const res = await fetch(`${API_BASE}/safety/live`);
    if (!res.ok) throw new Error('Failed to load safety state');
    return res.json();
  },

  async getSafetyEvents(machineId?: string) {
    const url = machineId ? `${API_BASE}/safety/events?machine_id=${machineId}` : `${API_BASE}/safety/events`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to load safety events');
    return res.json();
  },

  // Incidents
  async getIncidents(severity?: string, machineId?: string, resolved?: boolean): Promise<IncidentItem[]> {
    const params = new URLSearchParams();
    if (severity) params.append('severity', severity);
    if (machineId) params.append('machine_id', machineId);
    if (resolved !== undefined) params.append('resolved', String(resolved));
    const res = await fetch(`${API_BASE}/incidents?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to load incidents');
    return res.json();
  },

  async createIncident(incident: {
    machine_id: string;
    operator_id: string;
    incident_type: string;
    severity: string;
    description: string;
    location: string;
  }): Promise<IncidentItem> {
    const res = await fetch(`${API_BASE}/incidents`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(incident)
    });
    if (!res.ok) throw new Error('Failed to create incident');
    return res.json();
  },

  async updateIncident(incidentId: string, resolved: boolean, resolution?: string): Promise<IncidentItem> {
    const res = await fetch(`${API_BASE}/incidents/${incidentId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ resolved, resolution })
    });
    if (!res.ok) throw new Error('Failed to update incident');
    return res.json();
  },

  async getIncidentAnalytics() {
    const res = await fetch(`${API_BASE}/incidents/analytics/summary`);
    if (!res.ok) throw new Error('Failed to load incident analytics');
    return res.json();
  },

  // Anomalies
  async getAnomalies(machineId?: string): Promise<AnomalyItem[]> {
    const url = machineId ? `${API_BASE}/anomalies?machine_id=${machineId}` : `${API_BASE}/anomalies`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to load anomalies');
    return res.json();
  },

  // Training
  async getTraining(operatorId = 'OP001'): Promise<{ courses: TrainingCourse[]; recommendations: any[] }> {
    const res = await fetch(`${API_BASE}/training?operator_id=${operatorId}`);
    if (!res.ok) throw new Error('Failed to load training courses');
    return res.json();
  },

  async submitQuiz(courseId: string, operatorId: string, answers: Record<number, number>) {
    const res = await fetch(`${API_BASE}/training/${courseId}/quiz`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ operator_id: operatorId, answers })
    });
    if (!res.ok) throw new Error('Failed to submit quiz');
    return res.json();
  },

  // AI Assistant
  async getAssistantStatus(): Promise<AssistantStatus> {
    const res = await fetch(`${API_BASE}/assistant/status`);
    if (!res.ok) throw new Error('Failed to load assistant status');
    return res.json();
  },

  async queryAssistant(query: string, operatorId = 'OP001', machineId = 'EXC001'): Promise<AssistantQueryResponse> {
    const res = await fetch(`${API_BASE}/assistant/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, operator_id: operatorId, machine_id: machineId })
    });
    if (!res.ok) throw new Error('Failed to query assistant');
    return res.json();
  },

  // Simulation Controls
  async injectHazard(hazardType: string, machineId = 'EXC001', operatorId = 'OP001') {
    const res = await fetch(`${API_BASE}/simulation/inject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hazard_type: hazardType, machine_id: machineId, operator_id: operatorId })
    });
    if (!res.ok) throw new Error('Failed to inject hazard');
    return res.json();
  },

  async resetSimulation() {
    const res = await fetch(`${API_BASE}/simulation/reset`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to reset simulation');
    return res.json();
  },

  // Reports
  async getReport(reportType: string, operatorId = 'OP001', machineId = 'EXC001') {
    const res = await fetch(`${API_BASE}/reports/generate?report_type=${reportType}&operator_id=${operatorId}&machine_id=${machineId}`);
    if (!res.ok) throw new Error('Failed to generate report');
    return res.json();
  },

  // ML Metrics
  async getModelMetrics() {
    const res = await fetch(`${API_BASE}/predictions/metrics`);
    if (!res.ok) throw new Error('Failed to load ML metrics');
    return res.json();
  }
};
