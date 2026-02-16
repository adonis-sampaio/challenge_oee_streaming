import time
from src.services.model_storage import ModelStorage
from src.ml.feature_engineering import FeatureExtractor

class Predictor:
    def __init__(self):
        self.extractor = FeatureExtractor()

    def predict(self, series_id: str, window_data: list):
        start_time = time.time()
        
        pipeline = ModelStorage.load_pipeline(series_id)
        if not pipeline or len(window_data) < 10: # Mínimo de dados para features
            return "unknown", False, 0.0

        features = self.extractor.extract_features(window_data)
        
        state = pipeline['model_state'].predict(features)[0]
        piece_event = bool(pipeline['model_piece'].predict(features)[0])
        
        latency = (time.time() - start_time) * 1000
        return state, piece_event, latency