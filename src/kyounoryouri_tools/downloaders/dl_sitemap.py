from pathlib import Path

from .utils import download


def dl_sitemap(sitemap_url: str, sitemap_dir: Path) -> None:
    """
    Download recipe.xml

    Args:
        sitemap_url (str): url of recipe.xml
        sitemap_dir (Path): directory path to save recipe.xml

    """
    download(sitemap_url, sitemap_dir, title="Sitemap")
