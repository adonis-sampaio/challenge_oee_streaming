from fastapi import FastAPI, HTTPException
from src.api.schemas import StreamingSample, PredictionResponse, TrainingResponse
from src.services.cache_manager import cache_manager
from src.ml.trainer import Trainer
from src.ml.predictor import Predictor
import time

app = FastAPI(title="OEE Real-Time Analytics API")
predictor = Predictor()

@app.post("/train/{series_id}", response_model=TrainingResponse)
async def train_model(series_id: str, data: dict):
    try:
        trainer = Trainer(series_id)
        metrics = trainer.train(data)
        return {
            "series_id": series_id,
            "model_version": "v1.0",
            "status": "trained",
            "metrics": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/stream", response_model=PredictionResponse)
async def predict_stream(sample: StreamingSample):
    # 1. Adiciona ao cache para manter a janela deslizante
    cache_manager.add_sample(sample.series_id, sample.model_dump())
    
    # 2. Recupera a janela atual
    window = cache_manager.get_window(sample.series_id)
    
    # 3. Predição
    state, piece_event, latency = predictor.predict(sample.series_id, window)
    
    return {
        "series_id": sample.series_id,
        "current_state": state,
        "piece_produced_event": piece_event,
        "model_version": "v1.0",
        "latency_ms": round(latency, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)