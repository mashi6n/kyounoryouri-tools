from pathlib import Path

from bs4 import BeautifulSoup

from kyounoryouri_tools.extractors.core import (
    extract_date,
    extract_main,
    extract_sub,
    extract_time_nutr,
    extract_title,
    extract_urls,
)
from kyounoryouri_tools.models import RawRecipe


def extract_recipe(html_path: Path) -> RawRecipe:
    """
    Extract recipe from the page

    Args:
        html_path (Path): path to the html file

    Returns:
        Recipe: recipe

    """
    html = html_path.read_text()
    soup = BeautifulSoup(html, "html.parser")

    ingredients, servings, pre_steps = extract_sub(soup)
    steps = extract_main(soup)
    title = extract_title(soup)
    html_url, image_url = extract_urls(soup)
    cook_time, nutrients = extract_time_nutr(soup)
    date = extract_date(soup)

    if len(html_path.stem.split("_")) != 2:
        raise ValueError(f"Invalid html file name: {html_path}")

    recipe_number, recipe_name = html_path.stem.split("_")

    return RawRecipe(
        id=f"{int(recipe_number):08d}_{recipe_name}",
        title=title,
        instruction=steps,
        preparation=pre_steps,
        ingredients=ingredients,
        nutrients=nutrients,
        servings=servings,
        cook_time=cook_time,
        broadcast_date=date,
        image_url=image_url,
        html_url=html_url,
    )
