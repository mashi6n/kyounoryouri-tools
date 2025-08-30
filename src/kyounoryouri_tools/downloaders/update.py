import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

import rich

from kyounoryouri_tools.config import PathConfig
from kyounoryouri_tools.models import Recipe

from .download import dl_sitemap
from .utils import get_urlset


def clean_outdated_files(config: PathConfig, sitemap_url: str) -> None:
    old_sitemap = config.web.sitemap_dir / "recipe.xml"
    with TemporaryDirectory() as temp_dir:
        dl_sitemap(sitemap_url, Path(temp_dir))
        new_sitemap = Path(temp_dir) / "recipe.xml"

        old_urlset = get_urlset(old_sitemap)
        new_urlset = get_urlset(new_sitemap)

        if old_urlset is None:
            rich.print(f"sitemap not found in [magenta]{old_sitemap}")
            rich.print("Skip cleaning outdated files.")
            return

        if new_urlset is None:
            rich.print(
                f"[yellow] Failed to get the latest recipe.xml from the URL: [magenta]{sitemap_url}"
            )
            return

        old_loc2lastmod = {url.loc: url.lastmod for url in old_urlset.url}
        new_loc2lastmod = {url.loc: url.lastmod for url in new_urlset.url}

        remove_html_candidates: list[Path] = []
        remove_json_candidates: list[Path] = []
        remove_img_candidates: list[Path] = []

        for loc, lastmod in old_loc2lastmod.items():
            if loc not in new_loc2lastmod:
                continue
            if lastmod < new_loc2lastmod[loc]:
                html_path = config.html_file_path(loc)
                remove_html_candidates.append(html_path)

                json_path = config.json_file_path(html_path)
                remove_json_candidates.append(json_path)

                recipe = Recipe.model_validate_json(json_path.read_text())
                img_path = config.img_file_path(recipe.image_url)
                remove_img_candidates.append(img_path)

        for html_path, json_path, img_path in zip(
            remove_html_candidates, remove_json_candidates, remove_img_candidates
        ):
            html_path.unlink(missing_ok=True)
            json_path.unlink(missing_ok=True)
            img_path.unlink(missing_ok=True)

        rich.print(f"Removed {len(remove_html_candidates)} outdated files.")
        shutil.move(new_sitemap, config.sitemap_file_path())
    rich.print("Cleaning outdated files completed.\n")
