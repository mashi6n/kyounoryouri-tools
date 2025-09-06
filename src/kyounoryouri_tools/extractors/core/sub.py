from bs4 import BeautifulSoup

from kyounoryouri_tools.extractors.utils import get_next_sibling, is_kenko_page
from kyounoryouri_tools.models import Ingredient, TitledStep

from ._sub import extract_ingredients, extract_preparation


def extract_sub(
    soup: BeautifulSoup,
) -> tuple[list[Ingredient], str, list[TitledStep]]:
    """
    Extract ingredients, servings, and preparation steps from the page

    Args:
        soup (BeautifulSoup): soup object of the page

    Returns:
        tuple[list[Ingredient], str, list[TitledStep]]: ingredients, servings, and preparation steps

    """
    ingrlist_tags = soup.select("#ingredients_list")
    if len(ingrlist_tags) != 1:
        err = f"unexpected ingredients len: {len(ingrlist_tags)}"
        raise ValueError(err)

    ingredients = extract_ingredients(ingrlist_tags[0])

    detail_header = (
        soup.select(
            "#main-col > div.kenko--detail-recipe > div.detail-sub > div.detail-recipe-heading",
        )
        if is_kenko_page(soup)
        else soup.select(
            "#main-col > div.recipe--detail-recipe > div.detail-sub > div.detail-recipe-heading",
        )
    )
    if len(detail_header) not in [1, 2]:
        err = f"unexpected detail_header len: {len(detail_header)}"
        raise ValueError(err)

    ingr_header = detail_header[0]
    s = get_next_sibling(ingr_header)
    if s is not None and s.name == "p":
        servings = s.get_text(strip=True).replace("(", "").replace(")", "")
    else:
        servings = ""

    if len(detail_header) == 1:
        return ingredients, servings, []

    preparation_header = detail_header[1]
    pre_steps = extract_preparation(preparation_header)

    return ingredients, servings, pre_steps
