import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from ml.data_preprocessing import TaskDataPreprocessor

class TaskTimePredictor:
    def __init__(self, model_type: str = "RandomForest"):
        self.model_type = model_type
        if model_type == "GradientBoosting":
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.08,
                random_state=42
            )
        else:
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        self.preprocessor = TaskDataPreprocessor()
        self.residual_std_ = 5.0 # fallback default std error

    def fit(self, X_df: pd.DataFrame, y: pd.Series):
        self.preprocessor.fit(X_df)
        X_trans = self.preprocessor.transform(X_df)
        self.model.fit(X_trans, y)

        preds = self.model.predict(X_trans)
        residuals = y.values - preds
        self.residual_std_ = float(np.std(residuals))
        return self

    def predict_one(self, task_data: dict) -> dict:
        """
        Infers task completion time with confidence interval and explainable factor attribution.
        """
        df = pd.DataFrame([task_data])
        X_trans = self.preprocessor.transform(df)
        pred = float(self.model.predict(X_trans)[0])
        pred_time = round(max(10.0, pred), 1)

        # 90% confidence interval ~ 1.645 * standard error
        margin = max(3.0, round(1.645 * self.residual_std_, 1))
        conf_lower = max(5.0, round(pred_time - margin, 1))
        conf_upper = round(pred_time + margin, 1)

        # Factor attribution engine
        factors = []

        weather = task_data.get("weather", "Sunny")
        weather_deltas = {
            "Rainy": 7.5,
            "Storm": 14.0,
            "Windy": 3.2,
            "Cloudy": 1.5,
            "Sunny": -2.0
        }
        w_delta = weather_deltas.get(weather, 0.0)
        factors.append({
            "name": f"Weather ({weather})",
            "delta_min": round(w_delta, 1),
            "reason": f"{'+' if w_delta >= 0 else ''}{w_delta:.1f} min due to {weather} site conditions"
        })

        skill = task_data.get("operator_skill", "Intermediate")
        skill_deltas = {
            "Expert": -6.5,
            "Intermediate": 0.0,
            "Beginner": 8.0
        }
        s_delta = skill_deltas.get(skill, 0.0)
        factors.append({
            "name": f"Operator Skill ({skill})",
            "delta_min": round(s_delta, 1),
            "reason": f"{'+' if s_delta >= 0 else ''}{s_delta:.1f} min due to {skill} operator efficiency"
        })

        age = float(task_data.get("machine_age", 2.0))
        age_delta = round((age - 2.0) * 1.8, 1)
        if abs(age_delta) > 0.5:
            factors.append({
                "name": f"Machine Age ({age:.1f} yrs)",
                "delta_min": age_delta,
                "reason": f"{'+' if age_delta >= 0 else ''}{age_delta:.1f} min due to machine wear & cycle speed"
            })

        load_cycles = int(task_data.get("load_cycles", 15))
        cycle_delta = round((load_cycles - 15) * 1.2, 1)
        if abs(cycle_delta) > 0.5:
            factors.append({
                "name": f"Load Cycles ({load_cycles})",
                "delta_min": cycle_delta,
                "reason": f"{'+' if cycle_delta >= 0 else ''}{cycle_delta:.1f} min due to material volume and cycle count"
            })

        return {
            "predicted_time_min": pred_time,
            "confidence_lower_min": conf_lower,
            "confidence_upper_min": conf_upper,
            "factors": factors,
            "model_name": f"{self.model_type}Regressor"
        }

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        X_trans = self.preprocessor.transform(X_test)
        preds = self.model.predict(X_trans)
        mae = float(mean_absolute_error(y_test, preds))
        rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
        r2 = float(r2_score(y_test, preds))
        return {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2": round(r2, 4)
        }

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str):
        return joblib.load(filepath)
