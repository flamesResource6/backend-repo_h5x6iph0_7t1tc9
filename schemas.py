"""
Database Schemas for Aquaculture App

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercased class name.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Pond(BaseModel):
    """
    Collection: pond
    Basic pond registry for managing measurements by pond.
    """
    name: str = Field(..., description="Pond identifier or name")
    species: Optional[str] = Field(None, description="Cultured species, e.g., tilapia, shrimp")
    area_m2: Optional[float] = Field(None, ge=0, description="Surface area in square meters")
    average_depth_m: Optional[float] = Field(None, ge=0, description="Average depth in meters")

class Measurement(BaseModel):
    """
    Collection: measurement
    Water quality snapshot for a pond.
    """
    pond_id: str = Field(..., description="Referenced pond _id as string")
    timestamp: Optional[datetime] = Field(None, description="Measurement time; server will set if missing")
    temp_c: Optional[float] = Field(None, description="Temperature in °C")
    do_mgL: Optional[float] = Field(None, description="Dissolved oxygen in mg/L")
    ph: Optional[float] = Field(None, description="pH value")
    salinity_ppt: Optional[float] = Field(None, description="Salinity in ppt (‰)")
    ammonia_mgL: Optional[float] = Field(None, description="Total ammonia nitrogen (TAN) in mg/L")
    nitrite_mgL: Optional[float] = Field(None, description="Nitrite-N in mg/L")
    alkalinity_mgL: Optional[float] = Field(None, description="Alkalinity as CaCO3 in mg/L")
