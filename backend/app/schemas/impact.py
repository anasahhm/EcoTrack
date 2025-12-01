from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ImpactInput(BaseModel):
    transport_method: str = Field(..., description="car, bus, bike, walk, ev")
    transport_km: float = Field(..., ge=0, description="Kilometers traveled")
    electricity_kwh: float = Field(..., ge=0, description="Electricity usage in kWh")
    water_liters: float = Field(..., ge=0, description="Water usage in liters")
    diet_type: str = Field(..., description="veg, mixed, heavy_meat")
    waste_kg: float = Field(..., ge=0, description="Waste generated in kg")

class ImpactResponse(BaseModel):
    id: str
    carbon_score: float
    water_score: float
    energy_score: float
    waste_score: float
    overall_rating: str
    tips: List[str]
    ai_analysis: Optional[str] = None  # NEW
    created_at: datetime

class ImpactHistory(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[ImpactResponse]