from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime

class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class Shipment(SQLModel, table=True):
    id: int =Field(default=None, primary_key=True)
    content: str
    weight: float = Field(le=25, ge=1, description="Weight must be between 1 and 25 kg")
    destination: int
    status: ShipmentStatus = Field(default=ShipmentStatus.placed)
    estimated_delivery: datetime