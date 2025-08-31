from pydantic import BaseModel


class Recipe(BaseModel):
    id: str
    title: str
    ingredients: list[str]
    instructions: list[str]
