from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class StreamingSample(BaseModel):
    series_id: str
    timestamp: int
    vibration_level: float
    power_draw: float
    temperature: float

class PredictionResponse(BaseModel):
    series_id: str
    current_state: str
    piece_produced_event: bool
    model_version: str
    latency_ms: float

class TrainingResponse(BaseModel):
    series_id: str
    model_version: str
    status: str
    metrics: Dict[str, Any]