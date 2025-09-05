from pathlib import Path
from typing import Annotated

import rich
from rich.tree import Tree
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
    data_root: Annotated[Path, Argument(help="path to root data directory")] = Path("./data"),
    sitemap_url: Annotated[
        str, Option(help="sitemap url of NHK KyounoRyouri site")
    ] = "https://www.kyounoryouri.jp/sitemaps/recipe.xml",
    overwrite: Annotated[
        bool, Option(help="overwrite existing sitemap file", is_flag=True, flag_value=True)
    ] = False,
) -> None:
    pc = PathConfig(root_dir=data_root)
    pc.print()
    pc.create_all_dirs()
    dl_sitemap(sitemap_url, pc.sitemap_dir, overwrite=overwrite)
    t = Tree("[green]:heavy_check_mark: Initialization completed!")
    t.add(f"Sitemap URL: [cyan]{sitemap_url}[/]")
    t.add(f"Root Data Directory: [cyan]{data_root.absolute()}[/]")
    rich.print(t)


@app.command(name="download", help="download recipe data from the website")
def download(
    data_root: Annotated[Path, Argument(help="path to root data directory")] = Path("./data"),
) -> None:
    pc = PathConfig(root_dir=data_root)
    pc.print()
    if not pc.sitemap_file_path().exists():
        rich.print("[yellow]sitemap.xml not found. Please run `init` command first.")
        return

    if not pc.exist_all():
        rich.print("[yellow]Some directories do not exist. Please run `init` command first.")
        return

    html_downloaded = dl_html(pc)
    raw_json_converted, json_converted = html_to_json(pc)
    image_downloaded = dl_image(pc)

    t = Tree("[green]:heavy_check_mark: Everything is downloaded and converted!")
    t.add(f"{html_downloaded} HTML files")
    t.add(f"{image_downloaded} images")
    t.add(f"{raw_json_converted} raw JSON files")
    t.add(f"{json_converted} ordinary JSON files")
    rich.print(t)


@app.command(name="update", help="update sitemap and remove outdated files")
def update(
    data_root: Annotated[Path, Argument(help="path to root data directory")] = Path("./data"),
    sitemap_url: Annotated[
        str, Option(help="sitemap url of NHK KyounoRyouri site")
    ] = "https://www.kyounoryouri.jp/sitemaps/recipe.xml",
    overwrite: Annotated[
        bool, Option(help="update sitemap and delete outdated files", is_flag=True, flag_value=True)
    ] = False,
) -> None:
    pc = PathConfig(root_dir=data_root)
    pc.print()
    if not pc.exist_all():
        rich.print("[yellow]Some directories do not exist! Please run `init` command first.")
        return

    remove_candidates = clean_outdated_files(pc, sitemap_url, dry_run=not overwrite)
    if remove_candidates == -1:
        return
    if remove_candidates == 0:
        rich.print("[green]:heavy_check_mark: No outdated files found. Everything is up-to-date!")
    elif not overwrite:
        t = Tree("Outdated files found.")
        t.add(f"{remove_candidates} files are outdated.")
        t.add("Run the command with --overwrite option to delete them.")
        rich.print(t)
    else:
        t = Tree("[green]:heavy_check_mark: Outdated files have been removed![/]")
        t.add(f"{remove_candidates} files have been removed.")
        t.add("Sitemap has been updated to the latest version.")
        rich.print(t)


def main() -> None:
    app()
