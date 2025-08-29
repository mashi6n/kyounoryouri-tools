from bs4 import BeautifulSoup

from kyounoryouri_tools.extractors.utils import is_kenko_page
from kyounoryouri_tools.models import Nutrient


def extract_time_nutr(soup: BeautifulSoup) -> tuple[str, list[Nutrient]]:
    detail_elm = (
        soup.select(
            "#main-col > div.kenko--detail-main > div.detail-main-row > div.detail-col > div.recipes",  # noqa: E501
        )
        if is_kenko_page(soup)
        else soup.select(
            "#main-col > div.recipe--detail-main > div > div.detail-col > div.recipes",
        )
    )
    if len(detail_elm) != 1:
        err = f"unexpected detail len: {len(detail_elm)}"
        raise ValueError(err)

    detail_tag = detail_elm[0]

    cook_time = ""
    energy, salt = None, None
    for r in detail_tag.select("div"):
        p_tag = r.select("p")
        note = ""

        if len(p_tag) == 1:
            note = p_tag[0].get_text(strip=True).replace("＊", "")
            p_tag[0].decompose()

        elif len(p_tag) > 1:
            err = f"unexpected p_tag len: {len(p_tag)}"
            raise ValueError(err)

        content = r.get_text(strip=True)

        if "エネルギー" in content:
            quantity = content.split("／")[-1] if len(content.split("／")) > 1 else ""
            energy = Nutrient(
                name="energy",
                quantity=quantity,
                servings=note,
            )
        elif "塩分" in content and len(content.split("／")) > 1:
            salt = Nutrient(
                name="salt",
                quantity=content.split("／")[-1],
                servings=note,
            )
        elif "食塩相当量" in content:
            salt = Nutrient(
                name="salt",
                quantity=content.replace("食塩相当量", ""),
                servings=note,
            )
        elif "調理時間" in content:
            if len(content.split("／")) > 1:
                cook_time = content.split("／")[-1]
        else:
            err = f"unknown content: {content}"
            raise ValueError(err)

    return cook_time, [a for a in [energy, salt] if a is not None]
