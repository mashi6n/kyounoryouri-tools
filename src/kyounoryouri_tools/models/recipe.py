from pydantic import BaseModel


class Recipe(BaseModel):
    """
    An ordinary recipe data model.

    Fields:
        id (str): Unique identifier for the recipe. Formatted as \
            `{8-DIGIT-NUMBER}_{JAPANESE-RECIPE-TITLE}`.
        title (str): Title of the recipe in Japanese.
        ingredients (list[str]): List of ingredients required for the recipe in Japanese.\
            Hierarchical ingredients are flattened into a single list.
            E.g.
            ```
                A (marinade)
                  ├── soy sauce (1 cup)
                  └── sugar (2 tbsp)
            ```
            becomes
            ```
                - [A (marinade)] soy sauce (1 cup)
                - [A (marinade)] sugar (2 tbsp)
            ```
        instructions (list[str]): List of step-by-step instructions in Japanese.\
            Does not include step number.
    """

    id: str
    title: str
    ingredients: list[str]
    instructions: list[str]
