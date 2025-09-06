from __future__ import annotations

import datetime

from pydantic import BaseModel

from .recipe import Recipe


class RawRecipe(BaseModel):
    """
    A recipe data extracted from a html file.

    Fields:
        id (str): Unique identifier for the recipe. Formatted as \
            `{8-DIGIT-NUMBER}_{JAPANESE-RECIPE-TITLE}`.

        title (str): Title of the recipe in Japanese.

        instruction (list[TitledStep]): Hierarchical step-by-step instructions of the recipe\
            in Japanese.\
            Each section may have a title and contains multiple steps.\
            If the recipe does not have section title at all, it will have a single section\
            with an empty title and the section have all instruction steps in it.\

        preparation (list[TitledStep]): Hierarchical preparation steps of the recipe\
            in Japanese. Same structure as `instruction`.

        ingredients (list[Ingredient]): List of ingredients of the recipe in Japanese.\
            Ingredient have sub-ingredients to represent hierarchical ingredients.

        nutrients (list[Nutrient]): List of nutrients of the recipe in Japanese.\
            Each nutrient have name, quantity, and servings.

        servings (str): Information of servings in Japanese.

        cook_time (str): Cook time in Japanese. Contains units.

        broadcast_date (datetime.date): Date of broadcasting.

        image_url (str): URL of the image (thumbnail) for the final dish.
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
        """Return a list of step descriptions."""
        s = []
        for titled_step in self.instruction:
            for step in titled_step.steps:
                s.append(f"{step.step_num}. {step.desc}")
        return s

    def desc_contains(self, s: str) -> bool:
        """Check if any step description contains the given string."""
        for titled_step in self.instruction:
            for step in titled_step.steps:
                if s in step.desc:
                    return True
        return False

    def to_recipe(self) -> Recipe:
        """Convert RawRecipe to Recipe."""
        title = self.title
        ingredients = self.ingredients
        ingredient_list_str = []
        for ingr in ingredients:
            ingredient_list_str.extend(ingr.get_list_str(prefix=""))
        instruction = self.instruction
        instruction_list_str = []
        for instr in instruction:
            instruction_list_str.extend(
                instr.get_list_str_wo_title(remove_stepref_marker=True, assign_step_number=False)
            )

        return Recipe(
            id=self.id,
            title=title,
            ingredients=ingredient_list_str,
            instructions=instruction_list_str,
        )


class Ingredient(BaseModel):
    """
    An ingredient containing possible sub-ingredients.

    Fields:
        name (str): Name of the ingredient in Japanese.
        quantity (str): Quantity of the ingredient in Japanese.
        note (str): Note for the ingredient in Japanese.
        sub_ingr (list[Ingredient]): Sub ingredients which consist of the ingredient.
    """

    name: str
    quantity: str
    note: str
    sub_ingr: list[Ingredient]

    def get_list_str(self, prefix: str) -> list[str]:
        """Extract a flattened list of ingredient strings including sub-ingredients."""
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
    Nutrient information.

    Fields:
        name (str): name of the nutrient in Japanese.
        quantity (str): quantity of the nutrient in Japanese.
        servings (str): information of servings in Japanese.
    """

    name: str
    quantity: str
    servings: str


class TitledStep(BaseModel):
    """
    A section containing title and multiple instruction steps.

    Fields:
        title (str): Title of the section. May be empty
        steps (list[Step]): Steps in the section.
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
        """
        Get a list of step descriptions without the title.

        Args:
            remove_stepref_marker (bool): Whether to remove the step reference marker. \
                E.g. "Put __2__ on the plate." -> "Put 2 on the plate."
            assign_step_number (bool): Whether to assign step numbers to the descriptions.

        Returns:
            list[str]: A list of step descriptions.

        """
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


class Step(BaseModel):
    """
    A single step in a recipe instruction or preparation.

    Fields:
        step_num (int): step number. Starts from 1 in each recipe.
        desc (str): description of the step.
        point (str): tip, hint, or note for the step. May be empty.
    """

    step_num: int
    desc: str
    point: str

    def __str__(self) -> str:
        if self.point == "":
            return f"{self.step_num}: {self.desc}"
        return f"{self.step_num}: {self.desc}  [[!{self.point}]]"
