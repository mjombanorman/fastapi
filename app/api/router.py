from fastapi import APIRouter
from typing import Any
from fastapi import HTTPException, status
from app.api.dependencies import ServiceDep
from app.api.schema.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

router = APIRouter()


# get shipment by id
@router.get("/shipment")
async def get_shipment(id: int, service: ServiceDep) -> ShipmentRead:
    shipment = await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist"
        )
    return ShipmentRead.model_validate(shipment.__dict__)


# create shipment
@router.post("/shipment")
async def submit_shipment(
    shipment: ShipmentCreate, service: ServiceDep
) -> dict[str, Any]:
    new_shipment = await service.add(shipment)
    return {"detail": f"Shipment {new_shipment.id} is successfully created!"}


# update shipment status
@router.patch("/shipment")
async def update_shipment_status(
    id: int, shipment_update: ShipmentUpdate, service: ServiceDep
) -> ShipmentRead:
    if service.get(id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist"
        )

    updated_shipment = await service.update(id, shipment_update)
    return ShipmentRead.model_validate(updated_shipment.__dict__)


# delete shipment
@router.delete("/shipment")
async def delete_shipment(id: int, service: ServiceDep) -> dict[str, Any]:
    if service.get(id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist"
        )
    return await service.delete(id)  # type: ignore
