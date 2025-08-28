from pathlib import Path

from .utils import download, get_urlset


def dl_html(sitemap_dir: Path, html_dir: Path) -> None:
    """
    Download html files which are listed in recipe.xml

    Args:
        sitemap_dir (Path): directory path where recipe.xml is saved
        html_dir (Path): directory path to save html files

    """
    xml_path = sitemap_dir / "recipe.xml"
    urlset = get_urlset(xml_path)
    if urlset is None:
        return

    url_list = [url.loc for url in urlset.url]

    download(url_list, html_dir, title="HTML files")
