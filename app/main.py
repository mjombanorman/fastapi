from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep, create_db_and_tables
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")
  
app = FastAPI(lifespan=lifespan_handler)


@app.get("/shipment",response_model=ShipmentRead)
def get_shipment(id: int,session: SessionDep) -> ShipmentRead:
    
    shipment = session.get(Shipment,id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist")
    return ShipmentRead.model_validate(shipment)


@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate,session:SessionDep) -> dict[str, Any]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=7)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id": new_shipment.id}


@app.patch("/shipment",response_model=ShipmentRead)
def update_shipment_status(id: int, shipment_update:ShipmentUpdate,session:SessionDep)-> ShipmentRead | None:
   
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")  
    
    shipment = session.get(Shipment,id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist")
    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return ShipmentRead.model_validate(shipment)

@app.delete("/shipment")
def delete_shipment(id:int,session:SessionDep) -> dict[str, Any]:
    if session.get(Shipment,id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist")
    
    session.delete(session.get(Shipment,id))
    session.commit()
    
    return {"detail": f"shipment{id} is successfully deleted"}
   

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, # type: ignore
        title=app.title,
    )
