from pydantic import BaseModel,Field
from enum import Enum


class ShipmentStatus(str,Enum):
    placed ="placed"
    in_transit = "in transit"
    out_for_delivery = "out_for_delivery"
    delivered  = "delivered"

class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25, ge=1, description="Weight must be between 1 and 25 kg")
    destination: int | None = Field(default=None)


class ShipmentRead(BaseShipment):
      pass

class ShipmentCreate(BaseShipment):
      pass

class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(le=25, ge=1, description="Weight must be between 1 and 25 kg")
    destination: int | None = Field(default=None)
    status: ShipmentStatus
