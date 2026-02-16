from collections import deque
from typing import Dict, List
from src.config import WINDOW_SIZE

class CacheManager:
    def __init__(self):
        # Dicionário que armazena uma fila de tamanho fixo para cada máquina
        self._cache: Dict[str, deque] = {}

    def add_sample(self, series_id: str, sample: dict):
        if series_id not in self._cache:
            self._cache[series_id] = deque(maxlen=WINDOW_SIZE)
        
        self._cache[series_id].append(sample)

    def get_window(self, series_id: str) -> List[dict]:
        window = list(self._cache.get(series_id, []))
        return window

# Singleton para ser usado em toda a aplicação
cache_manager = CacheManager()