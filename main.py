from fastapi import FastAPI,status,HTTPException
from scalar_fastapi import get_scalar_api_reference # type: ignore
from typing import Any
from schemas import ShipmentRead, ShipmentCreate,ShipmentUpdate
from database import Database
app = FastAPI()
db=Database()

# @app.get("/shipment/latest")
# def get_latest_shipment()->dict[str,Any]:
#     id = max(shipments.keys())
#     return shipments[id]

@app.get("/shipment",response_model=ShipmentRead)
def get_shipment(id: int) -> ShipmentRead:
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist")
    return shipment


@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    new_id = db.create(shipment)
    return {"id": new_id}


@app.patch("/shipment",response_model=ShipmentRead)
def update_shipment_status(id: int, shipment:ShipmentUpdate)-> ShipmentRead | None:
    updated_shipment=db.update(id, shipment)

    if updated_shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist")
    return updated_shipment

@app.delete("/shipment")
def delete_shipment(id:int) -> dict[str, Any]:
    shipment = db.delete(id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist")
    
    return {"detail": f"shipment{id} is successfully deleted"}
   

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, # type: ignore
        title=app.title,
    )
