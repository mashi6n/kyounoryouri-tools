import datetime

from pydantic import BaseModel


class Url(BaseModel):
    """Url class corresponds to the `url` tag in sitemap.xml"""

    loc: str
    lastmod: datetime.date
    changefreq: str
    priority: float
