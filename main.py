from functools import lru_cache
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config import settings, db, RecipeModel, UpdateRecipeModel
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

# POST recipe
@app.post("/recipe", response_description="Add new recipe", response_model=RecipeModel)
async def create_recipe(recipe: RecipeModel = Body(...)):
    recipe = jsonable_encoder(recipe)
    new_recipe = await db["recipes"].insert_one(recipe)
    created_recipe = await db["recipes"].find_one({"_id": new_recipe.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_recipe)

# GET all recipes
@app.get(
    "/recipes", response_description="List all recipes", response_model=List[RecipeModel]
)
async def list_recipes():
    recipes = await db["recipes"].find().to_list(1000)
    return recipes

# GET recipe by _id
@app.get(
    "/recipe/{id}", response_description="Get a single recipe", response_model=RecipeModel
)
async def show_recipe(id: str):
    if (recipe := await db["recipes"].find_one({"_id": id})) is not None:
        return recipe

    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")

# PUT Recipe
@app.put("/recipe/{id}", response_description="Update a recipe", response_model=RecipeModel)
async def update_recipet(id: str, recipe: UpdateRecipeModel = Body(...)):
    recipe = {k: v for k, v in recipe.dict().items() if v is not None}

    if len(recipe) >= 1:
        update_result = await db["recipes"].update_one({"_id": id}, {"$set": recipe})

        if update_result.modified_count == 1:
            if (
                updated_recipe := await db["recipes"].find_one({"_id": id})
            ) is not None:
                return updated_recipe

    if (existing_recipe := await db["recipes"].find_one({"_id": id})) is not None:
        return existing_recipe

    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")

# DELETE Recipe
@app.delete("/recipe/{id}", response_description="Delete a recipe")
async def delete_recipe(id: str):
    delete_result = await db["recipes"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Recipe {id} not found")
