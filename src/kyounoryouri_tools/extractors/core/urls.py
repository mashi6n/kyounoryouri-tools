from urllib import parse

from bs4 import BeautifulSoup, Tag

from kyounoryouri_tools.extractors.utils import is_kenko_page


def extract_urls(soup: BeautifulSoup) -> tuple[str, str]:
    """
    Extract html url and thumbnail image url from the page

    Args:
        soup (BeautifulSoup): soup object of the page

    Returns:
        tuple[str, str]: tuple of html url and thumbnail image url.

    """
    thumbs = (
        soup.select("#main-col > div.kenko--detail-main > div.thumb > img")
        if is_kenko_page(soup)
        else soup.select("#main-col > div.recipe--detail-main > span > img")
    )

    if len(thumbs) != 1:
        err = f"unexpected thumb len: {len(thumbs)}"
        raise ValueError(err)
    thumb = thumbs[0]

    img_url_relative = thumb.get("src")
    if img_url_relative is None:
        err = "failed to extract img_url"
        raise ValueError(err)
    if isinstance(img_url_relative, list):
        img_url_relative = img_url_relative[0]
    img_url_wo_query = img_url_relative.split("?")[0]

    head = soup.head
    if head is None:
        err = "failed to extract head"
        raise ValueError(err)

    link_tag = head.find("link", rel="canonical")
    if link_tag is None or not isinstance(link_tag, Tag) or not link_tag.has_attr("href"):
        err = "failed to extract canonical link"
        raise ValueError(err)

    href = link_tag["href"]
    if isinstance(href, list):
        href = href[0]
    html_url = parse.urlparse(href)

    img_url = html_url.scheme + "://" + html_url.netloc + img_url_wo_query

    return html_url.geturl(), img_url
