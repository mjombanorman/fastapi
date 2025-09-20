from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from app.database.session import create_db_and_tables
from app.api.router import router



@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print("Starting up...")
    await create_db_and_tables()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan_handler)

app.include_router(router, prefix="/api/v1")
  


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, # type: ignore
        title=app.title,
    )
