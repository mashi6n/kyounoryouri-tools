from __future__ import annotations

from pydantic import BaseModel


class Ingredient(BaseModel):
    """
    Ingredient corresponds to an ingredient in a recipe.

    Fileds:
        name (str): name of the ingredient.
        quantity (str): quantity of the ingredient.
        note (str): note for the ingredient.
        sub_ingr (list[Ingredient]): sub ingredients which consist of the ingredient.
    """

    name: str
    quantity: str
    note: str
    sub_ingr: list[Ingredient]

    def get_list_str(self, prefix: str) -> list[str]:
        ingredient_list = []
        name = f"{prefix.strip()} {self.name}" if prefix != "" else self.name
        qty = f", 分量: {self.quantity}" if self.quantity != "" else ""
        note = f", 備考: {self.note}" if self.note != "" else ""
        if self.name.find("【") == -1:
            ingredient_list.append(name + qty + note)

        for sub_ingr in self.sub_ingr:
            ingredient_list.extend(sub_ingr.get_list_str(prefix=name))
        return ingredient_list
