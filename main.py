from fastapi import FastAPI
from config import settings
from enum import Enum
from typing import Union
import dotenv

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# predefined values test /models/alexnet
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return{"model_name" : model_name, "message": "Deep Learning FTW!"}
    if model_name == ModelName.lenet:
        return{"model_name" : model_name, "message": "HLeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# query params example /items/foo?short=False
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "short is false"})
    return item

# trying to use .env files records /info
@app.get("/info")
async def info():
    return {
         "app_name": settings.app_name,
         "admin_email": settings.admin_email
    }
