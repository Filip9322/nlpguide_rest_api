from functools import lru_cache
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config import settings, db, RecipeModel
from enum import Enum
from typing import Union, List
import dotenv

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/", response_description="Hello world")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}" , response_description="Say hello to name")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# predefined values test /models/alexnet
@app.get("/models/{model_name}", response_description="List all models")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return{"model_name" : model_name, "message": "Deep Learning FTW!"}
    if model_name == ModelName.lenet:
        return{"model_name" : model_name, "message": "HLeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# query params example /items/foo?short=False
@app.get("/items/{item_id}", response_description="List all items")
async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "short is false"})
    return item

# trying to use .env files records /info
@app.get("/info", response_description="List info test")
async def info():
    return {
         "app_name": settings.app_name,
         "admin_email": settings.admin_email,
         "mongodb_url": settings.mongodb_url
    }

# check DB for recipes
@app.get(
    "/recipes", response_description="List all recipes", response_model=List[RecipeModel]
)
async def list_recipes():
    recipes = await db["recipes"].find().to_list(1000)
    return recipes

# create recipe into DB
@app.post("/recipe", response_description="Add new student", response_model=RecipeModel)
async def create_recipe(recipe: RecipeModel = Body(...)):
    recipe = jsonable_encoder(recipe)
    new_recipe = await db["recipes"].insert_one(recipe)
    created_recipe = await db["recipes"].find_one({"_id": new_recipe.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_recipe)