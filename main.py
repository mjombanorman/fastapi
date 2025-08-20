from fastapi import FastAPI,status,HTTPException
from scalar_fastapi import get_scalar_api_reference # type: ignore
from typing import Any
from schemas import ShipmentRead, ShipmentCreate,ShipmentUpdate
from database import 
app = FastAPI()

@app.get("/shipment/latest")
def get_latest_shipment()->dict[str,Any]:
    id = max(shipments.keys())
    return shipments[id]

@app.get("/shipment",response_model=ShipmentRead)
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exist")
    return shipments[id]


@app.post("/shipment")
def submit_shipment(shipment: ShipmentCreate) -> dict[str, Any]:
    content = shipment.content
    weight = shipment.weight    
    new_id = max(shipments.keys()) + 1
    shipments[new_id] = {
        **shipment.model_dump(),
        "id": new_id,
        "status": "placed"
    }
    save_shipments_to_file()
    print(f"Shipment {new_id} with content '{content}' and weight {weight} kg has been created.")
    return {"id":new_id}


@app.patch("/shipment",response_model=ShipmentRead)
def update_shipment_status(id: int, body:ShipmentUpdate):
    shipment = shipments[id]
    shipment.update(body.model_dump(exclude_none=True))
    return shipment

@app.delete("/shipment")
def delete_shipment(id:int) -> dict[str, Any]:
    shipments.pop(id)
    return {"detail": f"shipment{id}is successfully deleted"}

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, # type: ignore
        title=app.title,
    )
