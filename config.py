from pydantic import BaseSettings
import motor.motor_asyncio
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List


class Settings(BaseSettings):
    env_file = '.env'
    env_file_encoding = 'utf-8'
    app_name: str = "NLPGuide"
    admin_email: str
    mongodb_url: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')


# Database Connection
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
db = client.nlpguide


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class RecipeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    recipe_cousine: str = Field(...)
    picture: str = Field(...)
    ingredients: str = Field(...)
    steps: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Frito Pie",
                "recipe_cousine": "western",
                "picture": "https://i0.wp.com/thegoodlifefrance.com/wp-content/uploads/2018/04/provencal-tomatoes.jpg?ssl=1",
                "ingredients": "1 pound ground beef, 2 cups shredded cheddar cheese",
                "steps": [
                    "1. Preheat oven to 350 degrees F.",
                    "2. Season your steak with salt and pepper.",
                    "3. Heat a pan over medium-high heat and cook steak for 3-4 minutes per side.",
                    "4. Transfer steak to a baking sheet and bake in preheated oven for 10-12 minutes.",
                    "5. Let steak rest for a few minutes before slicing and serving."
                ]
            }
        }

class UpdateRecipeModel(BaseModel):
    name: Optional[str]
    recipe_cousine: Optional[str]
    picture: Optional[str]
    ingredients: Optional[str]
    steps: List[str] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Frito Pie",
                "recipe_cousine": "western",
                "picture": "https://i0.wp.com/thegoodlifefrance.com/wp-content/uploads/2018/04/provencal-tomatoes.jpg?ssl=1",
                "ingredients": "1 pound ground beef, 2 cups shredded cheddar cheese",
                "steps": [
                    "1. Preheat oven to 350 degrees F.",
                    "2. Season your steak with salt and pepper.",
                    "3. Heat a pan over medium-high heat and cook steak for 3-4 minutes per side.",
                    "4. Transfer steak to a baking sheet and bake in preheated oven for 10-12 minutes.",
                    "5. Let steak rest for a few minutes before slicing and serving."
                ]
            }
        }