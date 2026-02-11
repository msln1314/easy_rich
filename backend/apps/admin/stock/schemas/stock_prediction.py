"""
Prediction-related data models for Kronos time series forecasting.
"""
from datetime import datetime
from core.data_types import DatetimeStr
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class PredictionPoint(BaseModel):
    """Single prediction point with date and predicted value."""
    date: str = Field(..., description="Prediction date in YYYY-MM-DD format")
    predicted_close: float = Field(..., description="Predicted closing price")


class ConfidenceInterval(BaseModel):
    """Confidence interval for a prediction point."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    lower_bound: float = Field(..., description="Lower confidence bound")
    upper_bound: float = Field(..., description="Upper confidence bound")


class PredictionOut(BaseModel):
    """Response model for stock price prediction."""
    stock_code: str = Field(..., description="Stock code that was predicted")
    prediction_days: int = Field(..., description="Number of days predicted")
    predictions: List[PredictionPoint] = Field(..., description="List of prediction points")
    confidence_intervals: List[ConfidenceInterval] = Field(..., description="Confidence intervals for predictions")
    historical_data_count: int = Field(..., description="Number of historical data points used")
    historical_data: List[Dict[str, Any]] = Field(..., description="Historical stock data used for prediction")
    created_at: DatetimeStr = Field(default_factory=datetime.now, description="Prediction creation timestamp")


class PredictionError(Exception):
    """Custom exception for prediction-related errors."""
    pass