from pydantic import BaseModel


class Nutrient(BaseModel):
    """
    Nutrient corresponds to a nutrient in a recipe.

    Fields:
        name (str): name of the nutrient.
        quantity (str): quantity of the nutrient.
        servings (str): information of servings.
    """

    name: str
    quantity: str
    servings: str
