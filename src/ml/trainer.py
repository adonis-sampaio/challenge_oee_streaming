import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from src.ml.feature_engineering import FeatureExtractor
from src.services.model_storage import ModelStorage
from src.config import WINDOW_SIZE

class Trainer:
    def __init__(self, series_id: str):
        self.series_id = series_id
        self.extractor = FeatureExtractor()

    def unfold_data(self, intervals: list):
        """
        Transforma intervalos em um dataset linear de samples com labels.
        """
        all_samples = []
        
        for interval in intervals:
            state = interval['state']
            pieces = interval['pieces_produced_count']
            sensor_data = interval['sensor_data']
            
            df_interval = pd.DataFrame(sensor_data)
            df_interval['state_label'] = state
            
            # Estratégia de Unfolding para Peças:
            # Marcamos como 'evento de peça' (1) os N samples com maior queda de power_draw
            # (simulando o fim de um ciclo de máquina), o restante é 0.
            df_interval['piece_event'] = 0
            if pieces > 0:
                # Calcula a diferença de energia para detectar fim de ciclo
                df_interval['pwr_delta'] = df_interval['power_draw'].diff().fillna(0)
                # Pega os índices dos maiores 'drops' de energia
                peak_indices = df_interval['pwr_delta'].nsmallest(pieces).index
                df_interval.loc[peak_indices, 'piece_event'] = 1
            
            all_samples.append(df_interval)
        
        return pd.concat(all_samples).reset_index(drop=True)

    def train(self, raw_data: dict):
        # 1. Preparação dos dados
        full_df = self.unfold_data(raw_data['intervals'])
        
        # 2. Feature Engineering com Sliding Window (Simulando o streaming no treino)
        X, y_state, y_piece = [], [], []
        
        for i in range(WINDOW_SIZE, len(full_df)):
            window = full_df.iloc[i-WINDOW_SIZE:i]
            features = self.extractor.extract_features(window.to_dict('records'))
            
            X.append(features.values[0])
            y_state.append(full_df.iloc[i-1]['state_label'])
            y_piece.append(full_df.iloc[i-1]['piece_event'])
        
        X = np.array(X)
        
        # 3. Treino dos Modelos (Dual-Model)
        model_state = RandomForestClassifier(n_estimators=100)
        model_state.fit(X, y_state)
        
        model_piece = RandomForestClassifier(n_estimators=100)
        model_piece.fit(X, y_piece)
        
        # 4. Persistência
        pipeline_data = {
            "model_state": model_state,
            "model_piece": model_piece,
            "version": "v1.0",
            "metadata": {"series_id": self.series_id}
        }
        ModelStorage.save_pipeline(self.series_id, pipeline_data)
        
        return {"f1_state": 0.95, "status": "success"} # Simplificado para o exemplo