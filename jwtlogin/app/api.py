from fastapi import FastAPI, Body,  Depends
from app.model import  UserSchema, UserLoginSchema,UserInput
from app.auth.auth_handler import signJWT

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

import databases
import sqlalchemy

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "users login"}

@app.post("/user/signup", dependencies=[Depends(JWTBearer())],)
async def create_user(req: UserInput):  # save user after login only :)
    query = login.insert().values(user_name=req.user_name, password=req.password,flag=req.flag)
    try:
        last_record_id = await database.execute(query)
    except:
        dic = {"error":"user_name already exits"}
        return dic
    else:
        dic = {**req.dict(), "id": last_record_id}
        return signJWT(dic)

async def check_user(data: UserInput):  # simple check with username and pass. that is it.
    query = login.select().where(login.c.user_name == data.user_name and login.c.password == data.password )
    user = await database.fetch_one(query)
    if  user is None:
        return False
    else:
        return True

@app.post("/user/login")                
async def user_login(user: UserInput):  # Username and Pass login check
    if await check_user(user):
        return signJWT(user.user_name)
    return {"error": "Wrong login details, Please check!"}

@app.post("/user/authenticate", dependencies=[Depends(JWTBearer())],)
def auth():                         # internal login check with token
    return{"results":"success"}



DATABASE_URL = "sqlite:///./login.db"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

login = sqlalchemy.Table(
    "login",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_name", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String), 
    sqlalchemy.Column("flag", sqlalchemy.String),
    sqlalchemy.UniqueConstraint('user_name', name='uix_1')
)
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

@app.on_event("startup")
async def startup():
    print("startup")
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    print("shutdown")
    await database.disconnect()

