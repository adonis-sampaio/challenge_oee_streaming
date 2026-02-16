import pandas as pd
import numpy as np

class FeatureExtractor:
    @staticmethod
    def extract_features(window_data: list) -> pd.DataFrame:
        """
        Transforma uma lista de samples (janela) em features estatísticas.
        """
        df = pd.DataFrame(window_data)
        
        if len(df) < 2:
            return pd.DataFrame() # Não há dados suficientes

        features = {}
        cols_to_process = ['vibration_level', 'power_draw', 'temperature']

        for col in cols_to_process:
            features[f'{col}_mean'] = df[col].mean()
            features[f'{col}_std'] = df[col].std()
            features[f'{col}_max'] = df[col].max()
            features[f'{col}_min'] = df[col].min()
            # Feature de tendência: valor atual vs média da janela
            features[f'{col}_delta'] = df[col].iloc[-1] - df[col].mean()

        return pd.DataFrame([features])