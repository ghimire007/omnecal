from fastapi import Depends, FastAPI
from config.database import create_start_app_handler, create_stop_app_handler
from sqlalchemy.orm import Session
from typing import Dict
from userService.v1.routers import userrouter
from companyService.v1.routers import companyrouter
from busService.v1.routers import busrouter


tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users and authentication",
    },
    {
        "name": "company",
        "description": "Operations with companies",
    },
    {
        "name": "bus",
        "description": "Operations with bus",
    },
]


app = FastAPI()
app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))
# userService.v1.models.Base.metadata.create_all(Engine)


app.include_router(userrouter, prefix="/api/v1")
app.include_router(companyrouter, prefix="/api/v1")
app.include_router(busrouter, prefix="/api/v1")


@app.get("/")
async def root(db: Session = Depends()) -> Dict:
    return {"message": "Hello Tom"}


"""
@app.post("/user/register")
async def createUser(request:UserSignup,response_model=UserResponse):
    query=usermodels.Users.insert().values(**request.dict())
    try:
       user_id=await database.execute(query)
       return {**request.dict(),"id":user_id}
    except Exception as e:
        print(e)

    return{"hello":"hello"}

"""
