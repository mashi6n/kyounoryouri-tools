from pathlib import Path
from typing import Annotated

import rich
import yaml
from rich.prompt import Confirm
from typer import Argument, Option, Typer

from kyounoryouri_tools.config import PathConfig
from kyounoryouri_tools.downloaders import clean_outdated_files, dl_html, dl_image
from kyounoryouri_tools.extractors import html_to_json

# from kyounoryouri_tools.nhkrecipe_text import create_nhkrecipe_text
# from kyounoryouri_tools.nhkrecipe_text_raw import create_nhkrecipe_text_raw

app = Typer(
    help=("Fetch and create dataset in Hugging Face Dataset format"),
    no_args_is_help=True,
)


# @app.command(name="create", help="Create NHKRecipe dataset in Hugging Face Dataset format")
# def create(
#     json_dir: Annotated[Path, Option(help="path to directory which contains json files")] = Path(
#         "data/json"
#     ),
#     dataset_dir: Annotated[Path, Option(help="path to output dateset directory")] = Path(
#         "data/dataset/nhkrecipe-text"
#     ),
# ) -> None:
#     if dataset_dir.exists():
#         rich.print("[bold yellow]:warning: Dataset already exists! :warning:")
#         rich.print(
#             "  If you want to re-create the dataset, please delete the existing dataset directory."
#         )
#         rich.print(f"  [magenta]{dataset_dir}")
#         return

#     rich.print({"json_dir": json_dir, "dataset_dir": dataset_dir})
#     if not Confirm.ask("Are you sure you want to create the dataset?"):
#         return

#     create_nhkrecipe_text(json_dir, dataset_dir)
#     rich.print("[bold green]:party_popper: Dataset created! :party_popper:")


# @app.command(name="create-raw", help="Create NHKRecipe dataset in Hugging Face Dataset format")
# def create_raw(
#     json_dir: Annotated[Path, Option(help="path to directory which contains json files")] = Path(
#         "data/json"
#     ),
#     dataset_dir: Annotated[Path, Option(help="path to output dateset directory")] = Path(
#         "data/dataset/nhkrecipe-raw-text"
#     ),
# ) -> None:
#     if dataset_dir.exists():
#         rich.print("[bold yellow]:warning: Dataset already exists! :warning:")
#         rich.print(
#             "  If you want to re-create the dataset, please delete the existing dataset directory."
#         )
#         rich.print(f"  [magenta]{dataset_dir}")
#         return

#     rich.print({"json_dir": json_dir, "dataset_dir": dataset_dir})
#     if not Confirm.ask("Are you sure you want to create the dataset?"):
#         return

#     create_nhkrecipe_text_raw(json_dir, dataset_dir)
#     rich.print("[bold green]:party_popper: Dataset created! :party_popper:")


@app.command(name="download", help="download recipe data from the website")
def download(
    config: Annotated[Path, Argument(help="path to output directory for htmls")] = Path(
        "config.yaml"
    ),
    sitemap_url: Annotated[
        str, Option(help="sitemap url of NHK KyounoRyouri site")
    ] = "https://www.kyounoryouri.jp/sitemaps/recipe.xml",
) -> None:
    if not Confirm.ask(f"Are you sure you want to fetch data from {sitemap_url}?"):
        return

    pc = PathConfig.model_validate(yaml.load(config.read_text(), Loader=yaml.SafeLoader))
    pc.create_all_dirs()

    clean_outdated_files(pc, sitemap_url)
    dl_html(pc)
    html_to_json(pc)
    dl_image(pc)

    rich.print("[bold green]:party_popper: Everything up-to-date! :party_popper:")


def main():
    app()
