import os

# Configurações de Janela Temporal
WINDOW_SIZE = 30  # segundos (ajuste conforme o tempo médio de produção de uma peça)

# Caminhos de Arquivos
MODEL_DIR = "models"
DATA_DIR = "data"

# Labels do Problema A
STATE_LABELS = ["producing", "idle", "downtime"]

# Garantir que a pasta de modelos existe
os.makedirs(MODEL_DIR, exist_ok=True)