
from pydantic import BaseModel
from sqlmodel import SQLModel,Field
from app.database.models import ShipmentStatus
from datetime import datetime


class BaseShipment(SQLModel):
    content: str
    weight: float = Field(le=25, ge=1, description="Weight must be between 1 and 25 kg")
    destination: int
  
class ShipmentRead(BaseShipment, table=False):
    id: int = Field(default=None, primary_key=True)
    status: ShipmentStatus
    estimated_delivery: datetime
     
class ShipmentCreate(BaseShipment):
      pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)
