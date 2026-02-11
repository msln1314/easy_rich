"""
Prediction-related data models for Kronos time series forecasting.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PredictionParams(BaseModel):
    """Request model for stock price prediction."""
    stock_code: str = Field(..., description="Stock code to predict")
    prediction_days: int = Field(default=7, ge=1, le=30, description="Number of days to predict")
    historical_days: int = Field(default=100, ge=30, le=1000, description="Number of historical days to use for prediction")
