import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from .ingredient import Ingredient
from .nutrient import Nutrient
from .titled_step import TitledStep


class Recipe(BaseModel):
    """
    Recipe corresponds to a recipe.

    Fields:
        id (str): id of the recipe.
        title (str): title of the recipe.
        instruction (list[TitledStep]): instruction of the recipe.
        preparation (list[TitledStep]): preparation of the recipe.
        ingredients (list[Ingredient]): ingredients of the recipe.
        nutrients (list[Nutrient]): nutrients of the recipe.
        servings (str): information of servings.
        cook_time (str): cook time.
        broadcast_date (datetime.date): date of broadcasting.
        image_url (str): url of the image of the recipe.
    """

    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str
    instruction: list[TitledStep]
    preparation: list[TitledStep]
    ingredients: list[Ingredient]
    nutrients: list[Nutrient]
    servings: str
    cook_time: str
    broadcast_date: datetime.date
    image_url: str
    html_url: str

    def list_description(self) -> list[str]:
        s = []
        for titled_step in self.instruction:
            for step in titled_step.steps:
                s.append(f"{step.step_num}. {step.desc}")
        return s

    def desc_contains(self, s: str) -> bool:
        for titled_step in self.instruction:
            for step in titled_step.steps:
                if s in step.desc:
                    return True
        return False
