export type UserRole = 'Operator' | 'Supervisor';

export interface TelemetryData {
  timestamp: string;
  machine_id: string;
  operator_id: string;
  task_id?: string;
  engine_hours: number;
  fuel_used_l: number;
  load_cycles: number;
  idling_time_min: number;
  engine_temperature: number;
  oil_pressure: number;
  hydraulic_pressure: number;
  engine_rpm: number;
  vibration: number;
  coolant_temperature: number;
  battery_voltage: number;
  load_weight: number;
  seatbelt_status: string;
  proximity_distance_m: number;
  worker_detected: boolean;
  safety_alert_triggered: boolean;
  fatigue_indicator: number;
  weather: string;
}

export interface RadarWorker {
  id: string;
  name: string;
  distance: number;
  angle: number;
  x: number;
  y: number;
  status: 'SAFE' | 'WARNING' | 'CRITICAL';
}

export interface SafetyAlert {
  rule_id: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  title: string;
  message: string;
  timestamp?: string;
}

export interface LiveTelemetryState {
  telemetry: TelemetryData;
  safety_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  status_label: 'SAFE' | 'WARNING' | 'HIGH RISK' | 'CRITICAL';
  active_alerts: SafetyAlert[];
  radar_objects: RadarWorker[];
  anomaly_detected: boolean;
  anomaly_details?: {
    is_anomaly: boolean;
    anomaly_score: number;
    risk_level: string;
    reason: string;
    factors: string[];
  };
  factor_breakdown?: Record<string, number>;
  advisory_disclaimer: string;
}

export interface TaskPredictionFactor {
  name: string;
  delta_min: number;
  reason: string;
}

export interface TaskPrediction {
  task_id: string;
  predicted_time_min: number;
  confidence_lower_min: number;
  confidence_upper_min: number;
  factors: TaskPredictionFactor[];
  model_name: string;
}

export interface TaskItem {
  task_id: string;
  task_type: string;
  machine_id: string;
  operator_id: string;
  location: string;
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  scheduled_start: string;
  estimated_time_min: number;
  predicted_time_min?: number;
  actual_time_min?: number;
  load_cycles: number;
  distance: number;
  weather: string;
  operator_skill: string;
  machine_age: number;
  status: 'Scheduled' | 'In Progress' | 'Completed' | 'Delayed' | 'Flagged';
  prediction_details?: TaskPrediction;
}

export interface MachineItem {
  machine_id: string;
  machine_type: string;
  machine_model: string;
  machine_age_years: number;
  engine_hours: number;
  maintenance_age_days: number;
  fuel_capacity: number;
  current_fuel_level: number;
  hydraulic_pressure: number;
  engine_temperature: number;
  engine_rpm: number;
  vibration_level: number;
  coolant_temperature: number;
  oil_pressure: number;
  battery_voltage: number;
  load_weight: number;
  operating_hours: number;
  location: string;
  status: string;
  health_score?: number;
  health_factors?: {
    temperature_health: number;
    vibration_health: number;
    oil_pressure_health: number;
    maintenance_health: number;
  };
}

export interface OperatorItem {
  operator_id: string;
  name: string;
  experience_years: number;
  skill_level: string;
  training_score: number;
  safety_score: number;
  average_task_accuracy: number;
  average_task_time: number;
  incident_count: number;
  fatigue_score: number;
  certification_status: string;
}

export interface IncidentItem {
  incident_id: string;
  timestamp: string;
  machine_id: string;
  operator_id: string;
  incident_type: string;
  severity: string;
  description: string;
  location: string;
  resolved: boolean;
  resolution?: string;
  created_at: string;
}

export interface AnomalyItem {
  anomaly_id: string;
  timestamp: string;
  machine_id: string;
  operator_id?: string;
  anomaly_score: number;
  risk_level: string;
  reason: string;
  factors: string[];
}

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  answer_idx: number;
}

export interface TrainingCourse {
  course_id: string;
  category: string;
  title: string;
  description: string;
  difficulty: string;
  duration_min: number;
  video_url?: string;
  quiz_questions?: QuizQuestion[];
  completion_status: 'Not Started' | 'In Progress' | 'Completed';
  score: number;
  attempts?: number;
}

export interface DashboardData {
  greeting: string;
  operator_name: string;
  current_machine_id: string;
  current_task?: TaskItem;
  task_progress_pct: number;
  estimated_remaining_time_min: number;
  machine_health_pct: number;
  safety_status: string;
  safety_score: number;
  risk_level: string;
  operator_status: string;
  weather: {
    condition: string;
    temperature_c: number;
    wind_speed_kmh: number;
    humidity_pct: number;
  };
  kpis: {
    today_tasks: number;
    completed_tasks: number;
    average_task_time: number;
    safety_alerts: number;
    idle_time_min: number;
    machine_utilization: number;
    fuel_efficiency_lh: number;
    training_progress_pct: number;
  };
  active_alerts: SafetyAlert[];
  safety_disclaimer: string;
}
