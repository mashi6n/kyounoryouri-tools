import time
from pathlib import Path
from urllib.parse import unquote

import requests
import rich
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeRemainingColumn, track

from kyounoryouri_tools.config import PathConfig
from kyounoryouri_tools.models import RawRecipe
from kyounoryouri_tools.utils import get_filepath_list

from .utils import get_urlset


def download(url: str | list[str], dir_path: Path, overwrite: bool = False) -> int:
    """
    Download file from `url` to `dir_path`.

    Args:
        url (str | list[str]): URL or list of URL to download
        dir_path (Path): directory path to save the file
        overwrite (bool, optional): If True, overwrite the file.\
            Otherwise, skip if the file exists. Defaults to False.

    Returns:
        int: The number of downloaded files.

    """
    url_list: list[str] = []
    download_url_list: list[str] = []

    if isinstance(url, str):
        url_list = [url]
    elif isinstance(url, list):
        url_list = url
    else:
        raise TypeError(f"Invalid type: {type(url)}")

    dir_path.mkdir(parents=True, exist_ok=True)

    if overwrite:
        download_url_list = url_list
    else:
        for u in url_list:
            save_file_path = dir_path / unquote(u.split("/")[-1])
            if not save_file_path.exists():
                download_url_list.append(u)

    with Progress(
        SpinnerColumn(),
        TextColumn("[white]{task.description}"),
        BarColumn(),
        TextColumn("[magenta]{task.completed}/" + str(len(download_url_list))),
        TextColumn("[gray]|"),
        TimeRemainingColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task("Downloading...", total=len(download_url_list))
        with requests.Session() as ss:
            for u in download_url_list:
                response = ss.get(u)
                save_file_path = dir_path / unquote(u.split("/")[-1])
                save_file_path.write_bytes(response.content)
                progress.update(task, advance=1)
                time.sleep(1)

    return len(download_url_list)


def dl_html(config: PathConfig) -> int:
    """
    Download html files which are listed in recipe.xml

    Args:
        config (PathConfig): Configuration object.

    Returns:
        int: The number of downloaded html files.

    """
    urlset = get_urlset(config.sitemap_file_path())
    if urlset is None:
        rich.print("[bold yellow]:warning: Failed to get urlset from sitemap.xml :warning:")
        return 0

    url_list = [url.loc for url in urlset.url][:10]

    downloaded = download(url_list, config.html_dir)
    rich.print(f"{downloaded} HTML files have been downloaded to [cyan]{config.html_dir}[/].\n")
    return downloaded


def dl_image(config: PathConfig) -> int:
    """
    Download thumbnail images whose urls are in json files

    Args:
        config (PathConfig): Configuration object.

    Returns:
        int: The number of downloaded images.

    """
    json_path_list = get_filepath_list(dir_path=config.raw_recipe_json_dir, ext="json")
    img_url_list = []

    for json_path in track(json_path_list, description="Collecting image URLs...", transient=True):
        d = RawRecipe.model_validate_json(json_path.read_text())
        img_url_list.append(d.image_url)
    downloaded = download(img_url_list, config.img_dir)
    rich.print(f"{downloaded} images have been downloaded to [cyan]{config.img_dir}[/].\n")
    return downloaded


def dl_sitemap(sitemap_url: str, sitemap_dir: Path, overwrite: bool = False) -> int:
    """
    Download recipe.xml

    Args:
        sitemap_url (str): url of recipe.xml
        sitemap_dir (Path): directory path to save recipe.xml
        overwrite (bool): If True, overwrite existing file.

    Returns:
        int: 1 if downloaded, 0 if skipped.

    """
    downloaded = download(sitemap_url, sitemap_dir, overwrite=overwrite)
    if downloaded == 1:
        rich.print(f"Sitemap file has been downloaded to [cyan]{sitemap_dir}[/].\n")
    else:
        rich.print(f"Sitemap file already exists at [cyan]{sitemap_dir}[/]. Skip downloading.\n")

    return downloaded
