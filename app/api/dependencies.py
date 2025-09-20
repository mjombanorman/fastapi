from app.services.shipment import ShipmentService
from app.database.session import AsyncSession, get_session
from fastapi import Depends
from typing import Annotated

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_shipment_service(session: SessionDep) -> ShipmentService:
    return ShipmentService(session)

ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
