import json
from pathlib import Path

import rich
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeRemainingColumn

from kyounoryouri_tools.utils import get_filepath_list

from .utils import download


def dl_image(json_dir: Path, img_dir: Path) -> None:
    """
    Download thumbnail images whose urls are in json files

    Args:
        json_dir (Path): directory path where json files are saved
        img_dir (Path): directory path to save images

    """
    json_path_list = get_filepath_list(dir_path=json_dir, ext="json")
    img_url_list = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[white]{task.description}"),
        BarColumn(),
        TextColumn("[magenta]{task.completed}/" + str(len(json_path_list))),
        TextColumn("[gray]|"),
        TimeRemainingColumn(),
        TextColumn("[cyan]remaining"),
        transient=True,
    ) as progress:
        task = progress.add_task("Collecting image URLs", total=len(json_path_list))
        for json_path in json_path_list:
            with json_path.open() as f:
                d = json.load(f)
                img_url = d["image_url"]
                img_url_list.append(img_url)
            progress.advance(task)
    rich.print("[bold green]:heavy_check_mark: [white]Collecting image URLs ... [yellow bold]Done!")
    download(img_url_list, img_dir, title="Images")
