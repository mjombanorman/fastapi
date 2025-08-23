from fastapi import Depends
from typing_extensions import Annotated
from sqlalchemy import create_engine
from sqlmodel import SQLModel,Session



engine = create_engine(
url="sqlite:///shipments.db",
echo=True,
connect_args={"check_same_thread": False}
)
def create_db_and_tables():
    
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(bind=engine) as session:
        yield session


SessionDep=Annotated[Session, Depends(get_session)]