from bs4 import Tag

from kyounoryouri_tools.models import Ingredient


def extract_ingredients(ingrlist_elm: Tag) -> list[Ingredient]:
    """
    Extract ingredients from the page

    Args:
        ingrlist_elm (Tag): Tag object of the ingredients list

    Returns:
        list[Ingredient]: list of ingredients

    """
    ingredients = []
    dl_list = ingrlist_elm.select("dl")
    for dl_tag in dl_list:
        dt_tag = dl_tag.find("dt")
        if not isinstance(dt_tag, Tag):
            err = f"we expect to find a tag, but type {type(dt_tag)} found"
            raise TypeError(err)

        if dt_tag.get("class") == ["point"]:
            # this item is a heading, not an ingredient
            ingredient_name = dt_tag.get_text(strip=True)
            quantity = ""
            note = ""
        else:
            ingr_quan_tag = dt_tag.find("span", class_="floatright")
            if not isinstance(ingr_quan_tag, Tag):
                err = f"we expect to find a tag, but type {type(ingr_quan_tag)} found"
                raise TypeError(err)

            quantity = ingr_quan_tag.get_text(strip=True)
            ingr_quan_tag.decompose()

            ingredient_name = dt_tag.get_text(strip=True).replace("・", "", 1)

            dd_tag = dl_tag.find("dd")
            if not isinstance(dd_tag, Tag):
                err = f"we expect to find a tag, but type {type(dd_tag)} found"
                raise TypeError(err)

            note = dd_tag.get_text(strip=True).replace("＊", "")

        dl_tag_class = dl_tag.get("class")
        if dl_tag_class is None:
            err = "we expect that dl tag has class attribute, but not found"
            raise ValueError(err)

        if "item1" in dl_tag_class:
            ingredients.append(
                Ingredient(name=ingredient_name, quantity=quantity, note=note, sub_ingr=[]),
            )
        elif "item2" in dl_tag_class:
            ingredients[-1].sub_ingr.append(
                Ingredient(name=ingredient_name, quantity=quantity, note=note, sub_ingr=[]),
            )
        elif "item3" in dl_tag_class:
            ingredients[-1].sub_ingr[-1].sub_ingr.append(
                Ingredient(name=ingredient_name, quantity=quantity, note=note, sub_ingr=[]),
            )
        else:
            err = f"unknown dl tag class: {dl_tag_class}"
            raise ValueError(err)

    return ingredients
