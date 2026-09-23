import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TASK_TYPES = [
    "Earth Excavation", "Trenching", "Material Loading",
    "Grading", "Demolition", "Compaction", "Hauling"
]

WEATHER_TYPES = ["Sunny", "Cloudy", "Rainy", "Windy", "Storm"]
SKILL_LEVELS = ["Beginner", "Intermediate", "Expert"]

class TaskDataPreprocessor:
    def __init__(self):
        self.encoder = OneHotEncoder(
            categories=[TASK_TYPES, WEATHER_TYPES, SKILL_LEVELS],
            sparse_output=False,
            handle_unknown="ignore"
        )
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        cat_features = df[["task_type", "weather", "operator_skill"]]
        self.encoder.fit(cat_features)

        num_features = df[[
            "machine_age", "load_cycles", "distance",
            "historical_operator_avg_time", "machine_utilization"
        ]]
        self.scaler.fit(num_features)
        self.is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Preprocessor has not been fitted yet.")
        cat_encoded = self.encoder.transform(df[["task_type", "weather", "operator_skill"]])
        num_scaled = self.scaler.transform(df[[
            "machine_age", "load_cycles", "distance",
            "historical_operator_avg_time", "machine_utilization"
        ]])
        return np.hstack([cat_encoded, num_scaled])

    def get_feature_names(self) -> list[str]:
        cat_names = list(self.encoder.get_feature_names_out(["task_type", "weather", "operator_skill"]))
        num_names = [
            "machine_age", "load_cycles", "distance",
            "historical_operator_avg_time", "machine_utilization"
        ]
        return cat_names + num_names
