from pydantic import BaseModel, Field

# This model ensures that if someone sends text instead of numbers,
# the API rejects it automatically.
class CelestialObject(BaseModel):
    ra: float = Field(..., description="Right Ascension (0-360)", ge=0, le=360)
    dec: float = Field(..., description="Declination (-90 to +90)", ge=-90, le=90)
    
class ClassificationResult(BaseModel):
    object_class: str
    confidence: float