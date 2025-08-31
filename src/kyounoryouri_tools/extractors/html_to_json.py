import rich
from rich.progress import track

from kyounoryouri_tools.config import PathConfig
from kyounoryouri_tools.extractors.extract_recipe import extract_recipe
from kyounoryouri_tools.utils import get_filepath_list


def html_to_json(config: PathConfig) -> None:
    """
    Extract recipe data from html and save as json

    Args:
        config (PathConfig): Configuration object.

    """
    html_path_list = get_filepath_list(dir_path=config.html_dir, ext="html")
    extract_html_list = []
    for html_path in html_path_list:
        json_path = config.raw_recipe_json_file_path(html_path)
        if not json_path.exists():
            extract_html_list.append(html_path)

    for html_path in track(
        extract_html_list, description="Extracting recipe from html...", transient=True
    ):
        raw_recipe = extract_recipe(html_path)
        raw_recipe_json_path = config.raw_recipe_json_file_path(html_path)
        raw_recipe_json_path.write_text(raw_recipe.model_dump_json(indent=4))

        recipe = raw_recipe.to_recipe()
        recipe_json_path = config.recipe_json_file_path(html_path)
        recipe_json_path.write_text(recipe.model_dump_json(indent=4))

    rich.print(f"Extracted {len(extract_html_list)} recipes.")
