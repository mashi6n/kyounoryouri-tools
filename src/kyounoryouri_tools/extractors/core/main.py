from bs4 import BeautifulSoup, Tag

from kyounoryouri_tools.extractors.utils import is_kenko_page
from kyounoryouri_tools.models import Step, TitledStep


def extract_main(soup: BeautifulSoup) -> list[TitledStep]:
    """
    Extract main steps from the page

    Args:
        soup (BeautifulSoup): soup object of the page

    Returns:
        list[TitledStep]: instruction. list of titled steps.

    """
    howto = (
        soup.select(
            "#main-col > div.kenko--detail-recipe > div.detail-main > div.detail-recipe-howto",
        )
        if is_kenko_page(soup)
        else soup.select(
            "#main-col > div.recipe--detail-recipe > div.detail-main > div.detail-recipe-howto",
        )
    )
    if len(howto) != 1:
        err = f"unexpected howto len: {len(howto)}"
        raise ValueError(err)

    howto_tag = howto[0]

    titledsteps = []
    for child in howto_tag.select("div"):
        child_class = child.get("class")
        if child_class is None:
            err = "howto-div child has no class attribute"
            raise ValueError(err)

        if child.name == "div" and "howto-ttl" in child_class:
            titledsteps.append(TitledStep(title=child.get_text(strip=True), steps=[]))

        elif child.name == "div" and "howto-sec" in child_class:
            step_number_tag = child.find("span")
            if not isinstance(step_number_tag, Tag):
                err = "failed to extract step number"
                raise ValueError(err)
            step_num = int(step_number_tag.get_text(strip=True))

            ps = child.select("p")
            if len(ps) not in [1, 2]:
                err = f"unexpected ps len: {len(ps)}"
                raise ValueError(err)

            num_elms = (
                ps[0].select("span.c-num.c-num-s.green")
                if is_kenko_page(soup)
                else ps[0].select("span.c-num.c-num-s")
            )
            for num_elm in num_elms:
                num_elm.replace_with(f"__{num_elm.get_text(strip=True)}__")
            desc = ps[0].get_text(strip=True)
            point = ps[1].get_text(strip=True) if len(ps) == 2 else ""

            if len(titledsteps) == 0:
                titledsteps.append(TitledStep(title="", steps=[]))
            titledsteps[-1].steps.append(
                Step(step_num=step_num, desc=desc, point=point),
            )
    return titledsteps
