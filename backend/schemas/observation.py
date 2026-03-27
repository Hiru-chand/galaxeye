from pydantic import BaseModel

class ObservationInput(BaseModel):
    u: float
    g: float
    r: float
    i: float
    z: float
    w1: float
    w2: float