from pathlib import Path

from rich.progress import track

from kyounoryouri_tools.extractors.extract_recipe import extract_recipe
from kyounoryouri_tools.utils import get_filepath_list


def html_to_json(html_dir: Path, json_dir: Path) -> None:
    """
    Extract recipe data from html and save as json

    Args:
        html_dir (Path): directory path where html files are saved
        json_dir (Path): directory path to save json files

    """
    json_dir.mkdir(parents=True, exist_ok=True)
    html_path_list = get_filepath_list(dir_path=html_dir, ext="html")
    extract_html_list = []
    for html_path in html_path_list:
        json_path = json_dir / (html_path.stem + ".json")
        if not json_path.exists():
            extract_html_list.append(html_path)

    for html_path in track(extract_html_list, description="Extracting recipe data"):
        recipe = extract_recipe(html_path)
        json_path = json_dir / (html_path.stem + ".json")
        with json_path.open("w") as f:
            f.write(recipe.model_dump_json(indent=4))
