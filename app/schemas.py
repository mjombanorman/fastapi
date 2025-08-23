from pydantic import BaseModel,Field
from app.database.models import ShipmentStatus
from datetime import datetime


class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25, ge=1, description="Weight must be between 1 and 25 kg")
    destination: int
  


class ShipmentRead(BaseShipment):
      pass

class ShipmentCreate(BaseShipment):
      pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
