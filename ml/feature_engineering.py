import pandas as pd
import numpy as np

def engineer_task_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers industrial task duration features:
    - task_base_duration_prior
    - weather_severity_index
    - machine_wear_index
    - operator_experience_factor
    """
    df = df.copy()

    # Weather impact baseline
    weather_impact = {
        "Sunny": 1.0,
        "Cloudy": 1.05,
        "Windy": 1.10,
        "Rainy": 1.25,
        "Storm": 1.45
    }
    df["weather_severity_index"] = df["weather"].map(lambda w: weather_impact.get(w, 1.0))

    # Skill factor
    skill_impact = {
        "Beginner": 1.20,
        "Intermediate": 1.0,
        "Expert": 0.85
    }
    df["operator_skill_factor"] = df["operator_skill"].map(lambda s: skill_impact.get(s, 1.0))

    # Machine wear index
    df["machine_wear_index"] = 1.0 + (df["machine_age"] * 0.03)

    return df

def engineer_telemetry_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers telemetry mechanical & behavioral features:
    - thermal_ratio (engine_temperature / coolant_temperature)
    - mechanical_stress_index (vibration * engine_rpm / 1000)
    - idle_ratio (idling_time_min / max(1.0, engine_hours * 60))
    """
    df = df.copy()
    coolant = df["coolant_temperature"].replace(0, np.nan).fillna(85.0)
    df["thermal_ratio"] = df["engine_temperature"] / coolant
    df["mechanical_stress_index"] = (df["vibration"] * df["engine_rpm"]) / 1000.0
    return df
