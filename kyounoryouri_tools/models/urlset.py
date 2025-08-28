from pydantic import BaseModel

from .url import Url


class Urlset(BaseModel):
    """Urlset class corresponds to the `urlset` tag in sitemap.xml"""

    url: list[Url]
