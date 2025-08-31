from pathlib import Path
from typing import Annotated

import rich
import yaml
from typer import Argument, Option, Typer

from kyounoryouri_tools.config import PathConfig
from kyounoryouri_tools.downloaders import clean_outdated_files, dl_html, dl_image, dl_sitemap
from kyounoryouri_tools.extractors import html_to_json

app = Typer(
    help=("Fetch and create dataset in Hugging Face Dataset format"),
    no_args_is_help=True,
)


@app.command(name="init", help="initialize directory structure and download sitemap file")
def init(
    config: Annotated[Path, Argument(help="path to output directory for htmls")] = Path(
        "config.yaml"
    ),
    sitemap_url: Annotated[
        str, Option(help="sitemap url of NHK KyounoRyouri site")
    ] = "https://www.kyounoryouri.jp/sitemaps/recipe.xml",
    overwrite: Annotated[
        bool, Option(help="overwrite existing sitemap file", is_flag=True, flag_value=True)
    ] = False,
) -> None:
    pc = PathConfig.model_validate(yaml.load(config.read_text(), Loader=yaml.SafeLoader))
    pc.print()
    pc.create_all_dirs()
    rich.print("Initialized directory structure.")
    dl_sitemap(sitemap_url, pc.sitemap_dir, overwrite=overwrite)


@app.command(name="download", help="download recipe data from the website")
def download(
    config: Annotated[Path, Argument(help="path to output directory for htmls")] = Path(
        "config.yaml"
    ),
) -> None:
    pc = PathConfig.model_validate(yaml.load(config.read_text(), Loader=yaml.SafeLoader))
    pc.print()
    if not pc.sitemap_file_path().exists():
        rich.print("[yellow]sitemap.xml not found! Please run `init` command first.")
        return

    if not pc.exist_all():
        rich.print("[yellow]Some directories do not exist! Please run `init` command first.")
        return

    dl_html(pc)
    html_to_json(pc)
    dl_image(pc)

    rich.print("[bold green]:party_popper: Everything up-to-date! :party_popper:")


@app.command(name="update", help="update sitemap and remove outdated files")
def update(
    config: Annotated[Path, Argument(help="path to output directory for htmls")] = Path(
        "config.yaml"
    ),
    sitemap_url: Annotated[
        str, Option(help="sitemap url of NHK KyounoRyouri site")
    ] = "https://www.kyounoryouri.jp/sitemaps/recipe.xml",
    overwrite: Annotated[
        bool, Option(help="update sitemap and delete outdated files", is_flag=True, flag_value=True)
    ] = False,
) -> None:
    pc = PathConfig.model_validate(yaml.load(config.read_text(), Loader=yaml.SafeLoader))
    pc.print()
    if not pc.exist_all():
        rich.print("[yellow]Some directories do not exist! Please run `init` command first.")
        return

    clean_outdated_files(pc, sitemap_url, dry_run=not overwrite)


def main() -> None:
    app()
