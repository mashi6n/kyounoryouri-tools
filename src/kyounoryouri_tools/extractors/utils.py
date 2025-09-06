from bs4 import BeautifulSoup, PageElement, Tag


def is_kenko_page(soup: BeautifulSoup) -> bool:
    """
    Check if the page is a 健康キッチン page

    Args:
        soup (BeautifulSoup): soup object of the page

    Returns:
        bool: True if the page is a 健康キッチン page

    """
    body = soup.body
    if body is None:
        err = "failed to extract body"
        raise ValueError(err)

    return body.has_attr("id") and body["id"] == "page-kenko"


def get_next_sibling(s: Tag | PageElement) -> Tag | None:
    """
    Get the next sibling which is not blank

    Args:
        s (Tag | PageElement): Tag or PageElement object

    Returns:
        PageElement | None: next sibling which is not blank

    """
    _s = s.next_sibling
    while _s is not None and not isinstance(_s, Tag):
        _s = _s.next_sibling
    return _s


def get_prev_sibling(s: Tag | PageElement) -> Tag | None:
    """
    Get the previous sibling which is not blank

    Args:
        s (Tag | PageElement): Tag or PageElement object

    Returns:
        PageElement | None: next sibling which is not blank

    """
    _s = s.previous_sibling
    while _s is not None and not isinstance(_s, Tag):
        _s = _s.previous_sibling
    return _s
