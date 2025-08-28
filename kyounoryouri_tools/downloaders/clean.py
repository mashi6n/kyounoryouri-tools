import json
import shutil
from pathlib import Path
from urllib.parse import unquote

import rich

from kyounoryouri_tools.models import Recipe, Urlset

from .dl_sitemap import dl_sitemap
from .utils import get_urlset


def clean_outdated_files(
    html_dir: Path, img_dir: Path, json_dir: Path, sitemap_dir: Path, sitemap_url: str
) -> None:
    old_sitemap_dir = sitemap_dir
    new_sitemap_dir = sitemap_dir / "tmp"
    dl_sitemap(sitemap_url, new_sitemap_dir)

    old_urlset = get_urlset(old_sitemap_dir / "recipe.xml")
    new_urlset = get_urlset(new_sitemap_dir / "recipe.xml")

    if new_urlset is None and old_urlset is None:
        err = f"Failed to get the latest recipe.xml from the URL:{sitemap_url}"
        err += f" Also, the recipe.xml is not found in {old_sitemap_dir}."
        raise ValueError(err)

    if new_urlset is None:
        rich.print(
            f"[yellow] Failed to get the latest recipe.xml from the URL: [magenta]{sitemap_url}"
        )
        new_urlset = Urlset(url=[])

    if old_urlset is None:
        rich.print(f"[yellow] recipe.xml is not found in [magenta]{old_sitemap_dir}.")
        old_urlset = Urlset(url=[])

    old_loc2lastmod = {url.loc: url.lastmod for url in old_urlset.url}
    new_loc2lastmod = {url.loc: url.lastmod for url in new_urlset.url}

    remove_htmls: list[Path] = []

    for loc, lastmod in old_loc2lastmod.items():
        if loc not in new_loc2lastmod:
            continue
        if lastmod < new_loc2lastmod[loc]:
            html_path = html_dir / unquote(loc.split("/")[-1])
            remove_htmls.append(html_path)

    for html_path in remove_htmls:
        json_path = json_dir / (html_path.stem + ".json")
        if not json_path.exists():
            continue
        with json_path.open() as f:
            d = json.load(f)
        recipe = Recipe.model_validate(d)
        img_url = recipe.image_url
        img_path = img_dir / unquote(img_url.split("/")[-1])

        html_path.unlink()
        json_path.unlink()
        img_path.unlink()
    rich.print(
        f"[bold green]:heavy_check_mark: [white]Removing outdated files ... [yellow bold]Done![white] {len(remove_htmls)} files are removed."  # noqa: E501
    )
    (old_sitemap_dir / "recipe.xml").unlink()
    shutil.move(new_sitemap_dir / "recipe.xml", sitemap_dir / "recipe.xml")
    shutil.rmtree(new_sitemap_dir)

    rich.print("[bold green]:heavy_check_mark: [white]Update recipe.xml ... [yellow bold]Done!")
