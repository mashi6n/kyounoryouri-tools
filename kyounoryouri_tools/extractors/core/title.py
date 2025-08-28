from bs4 import BeautifulSoup

from kyounoryouri_tools.extractors.utils import is_kenko_page


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract title from the page

    Args:
        soup (BeautifulSoup): soup object of the page

    Returns:
        str: title

    """
    h1_title = (
        soup.select(
            "#main-col > div.kenko--detail-heading > div.heading-main > div",
        )
        if is_kenko_page(soup)
        else soup.select(
            "#main-col > div.recipe--detail-heading > div.heading-main > div",
        )
    )

    if len(h1_title) != 1:
        err = f"unexpected h1 title len: {len(h1_title)}"
        raise ValueError(err)

    h1_title_tag = h1_title[0]
    title = h1_title_tag.get_text(strip=True)
    return title
