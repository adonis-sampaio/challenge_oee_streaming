import joblib
import os
from src.config import MODEL_DIR

class ModelStorage:
    @staticmethod
    def save_pipeline(series_id: str, pipeline_data: dict):
        path = os.path.join(MODEL_DIR, f"pipeline_{series_id}.joblib")
        joblib.dump(pipeline_data, path)

    @staticmethod
    def load_pipeline(series_id: str):
        path = os.path.join(MODEL_DIR, f"pipeline_{series_id}.joblib")
        if os.path.exists(path):
            return joblib.load(path)
        return None