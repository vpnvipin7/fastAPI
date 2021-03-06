from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel
from typing import List

from fastapi import FastAPI, Body,  Depends

from auth.auth_handler import signJWT

from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT

app = FastAPI()

class Order_model(BaseModel):
    order_number: str
    status: str

class Order(BaseModel):
    id: int
    order_number: str
    status: str

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("order_number", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String),
)
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


@app.get("/orders/", response_model=List[Order], dependencies=[Depends(JWTBearer())],)
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)

@app.post("/orders/", response_model=Order, dependencies=[Depends(JWTBearer())],)
async def create_orders(order: Order_model):
    query = orders.insert ().values(order_number=order.order_number, status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}

@app.on_event("startup")
async def startup():
    print("startup")
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    print("shutdown")
    await database.disconnect()
