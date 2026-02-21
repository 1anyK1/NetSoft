from pydantic import BaseModel
from typing import Optional

class CarsBase(BaseModel):
    model: str
    body: str
    year: int
    power: int
    description: Optional[str] = None

class CarCreate(CarsBase):
    pass

class Car(CarsBase):
    id: int
    class Config:
        from_attributes = True

