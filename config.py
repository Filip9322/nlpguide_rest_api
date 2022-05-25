from pydantic import BaseSettings
import motor.motor_asyncio
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


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
            }
        }

class UpdateRecipeModel(BaseModel):
    name: Optional[str]
    recipe_cousine: Optional[str]
    picture: Optional[str]
    ingredients: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Frito Pie",
                "recipe_cousine": "western",
                "picture": "https://i0.wp.com/thegoodlifefrance.com/wp-content/uploads/2018/04/provencal-tomatoes.jpg?ssl=1",
                "ingredients": "1 pound ground beef, 2 cups shredded cheddar cheese",
            }
        }