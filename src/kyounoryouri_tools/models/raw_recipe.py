from __future__ import annotations

import datetime

from pydantic import BaseModel

from .recipe import Recipe


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


class Step(BaseModel):
    """
    Step correspods to a single step in a recipe instruction or preparation.

    Fields:
        step_num (int): step number.
        desc (str): description of the step.
        point (str): tip, hint, or note for the step.
    """

    step_num: int
    desc: str
    point: str

    def __str__(self) -> str:
        if self.point == "":
            return f"{self.step_num}: {self.desc}"
        return f"{self.step_num}: {self.desc}  [[!{self.point}]]"


class TitledStep(BaseModel):
    """
    TitledStep corresponds to a section of a recipe instruction or preparation.

    Fields:
        title (str): title of the section. section may not have a title.
        steps (list[Step]): steps in the section.
    """

    title: str
    steps: list[Step]

    def __str__(self) -> str:
        s = self.title + "\n"
        for step in self.steps:
            s += f"  {step}\n"
        return s

    def get_list_str_wo_title(
        self, remove_stepref_marker: bool, assign_step_number: bool
    ) -> list[str]:
        step_list = []
        for step in self.steps:
            if assign_step_number:
                if remove_stepref_marker:
                    step_list.append(f"{step.step_num}. {step.desc.replace('__', '')}".strip())
                else:
                    step_list.append(f"{step.step_num}. {step.desc}".strip())
            else:
                if remove_stepref_marker:
                    step_list.append(step.desc.replace("__", "").strip())
                else:
                    step_list.append(step.desc.strip())
        return step_list


class RawRecipe(BaseModel):
    """
    RawRecipe corresponds to a recipe data extracted from the website.

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

    id: str
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

    def to_recipe(self) -> Recipe:
        title = self.title
        ingredients = self.ingredients
        ingredient_list_str = []
        for ingr in ingredients:
            ingredient_list_str.extend(ingr.get_list_str(prefix=""))
        instruction = self.instruction
        instruction_list_str = []
        for instr in instruction:
            instruction_list_str.extend(
                instr.get_list_str_wo_title(remove_stepref_marker=True, assign_step_number=True)
            )

        return Recipe(
            id=self.id,
            title=title,
            ingredients=ingredient_list_str,
            instructions=instruction_list_str,
        )
