import datetime

from bs4 import BeautifulSoup

from kyounoryouri_tools.extractors.utils import get_prev_sibling, is_kenko_page


def extract_date(soup: BeautifulSoup) -> datetime.date:
    share_tags = (
        soup.select(
            "#main-col > div.recipe--detail-share.kenko--detail-share",
        )
        if is_kenko_page(soup)
        else soup.select("#main-col > div.recipe--detail-share")
    )
    if len(share_tags) != 1:
        err = f"unexpected share len: {len(share_tags)}"
        raise ValueError(err)

    share_tag = share_tags[0]

    a = get_prev_sibling(share_tag)
    if a is None:
        err = "failed to extract a"
        raise ValueError(err)

    divs = a.select("div")
    if len(divs) < 2:
        err = f"unexpected divs len: {len(divs)}"
        raise ValueError(err)

    s = divs[1].select("span")
    if len(s) < 1:
        err = f"unexpected span len: {len(s)}"
        raise ValueError(err)

    return (
        datetime.datetime.strptime(s[0].get_text(strip=True), "%Y/%m/%d")
        .astimezone(datetime.timezone(datetime.timedelta(hours=9)))
        .date()
    )
