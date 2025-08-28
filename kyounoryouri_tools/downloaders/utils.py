import time
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests
import rich
import xmltodict
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeRemainingColumn

from kyounoryouri_tools.models import Urlset


def get_urlset(xml_source: Path | str) -> Urlset | None:
    """
    Get urlset from xml file

    Args:
        xml_source (Path | str): path or url to xml file

    Returns:
        Urlset | None: urlset, None if xml_source is invalid

    """
    if isinstance(xml_source, str):
        err = "URL is not supported."
        raise NotImplementedError(err)
        try:
            urlparse(xml_source)
        except ValueError:
            print(f"{xml_source} is not a valid URL.")
            return None
        res = requests.get(xml_source, timeout=10)
        xmldict = xmltodict.parse(res.content)

    if isinstance(xml_source, Path):
        if not xml_source.exists():
            print(f"{xml_source} does not exist.")
            return Urlset(url=[])
        with xml_source.open() as f:
            xmldict = xmltodict.parse(f.read())

    urlset_dict = xmldict["urlset"]
    for k in list(urlset_dict.keys()):
        if k != "url":
            urlset_dict.pop(k)

    urlset = Urlset.model_validate(urlset_dict)

    return urlset


def download(
    url: str | list[str], dir_path: Path, overwrite: bool = False, title: str = ""
) -> None:
    """
    Download file from `url` to `dir_path`. If file already exists, skip downloading.

    Args:
        url (str | list[str]): URL or list of URL to download
        dir_path (Path): directory path to save the file
        overwrite (bool, optional): If True, overwrite the file. Defaults to False.
        title (str, optional): Title of the progress bar. Defaults to "".

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
        TextColumn("[cyan]remaining"),
        transient=True,
    ) as progress:
        task = progress.add_task(f"Downloading {title}", total=len(download_url_list))
        with requests.Session() as ss:
            for u in download_url_list:
                response = ss.get(u)
                save_file_path = dir_path / unquote(u.split("/")[-1])
                with save_file_path.open("wb") as f:
                    f.write(response.content)
                progress.update(task, advance=1)
                time.sleep(1)
    rich.print(f"[bold green]:heavy_check_mark: [white]Downloading {title} ... [yellow bold]Done!")
