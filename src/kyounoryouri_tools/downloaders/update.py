import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

import rich
from rich.progress import track
from rich.prompt import Confirm

from kyounoryouri_tools.config import PathConfig
from kyounoryouri_tools.models import Recipe

from .download import dl_sitemap
from .utils import get_urlset


def clean_outdated_files(config: PathConfig, sitemap_url: str, dry_run: bool = True) -> int:  # noqa: C901
    """
    Download the latest sitemap and clean outdated files.

    Args:
        config (PathConfig): Configuration object.
        sitemap_url (str): URL of the sitemap.
        dry_run (bool): If True, perform a dry run without making changes
                        and return the number of outdated files.

    Returns:
        int: The number of outdated files.

    """
    old_sitemap = config.web.sitemap_dir / "recipe.xml"
    with TemporaryDirectory() as temp_dir:
        dl_sitemap(sitemap_url, Path(temp_dir))
        new_sitemap = Path(temp_dir) / "recipe.xml"

        old_urlset = get_urlset(old_sitemap)
        new_urlset = get_urlset(new_sitemap)

        if old_urlset is None:
            rich.print(f"sitemap not found in [magenta]{old_sitemap}")
            rich.print("Skip cleaning outdated files.")
            return 0

        if new_urlset is None:
            rich.print(
                f"[yellow] Failed to get the latest recipe.xml from the URL: [magenta]{sitemap_url}"
            )
            return 0

        old_loc2lastmod = {url.loc: url.lastmod for url in old_urlset.url}
        new_loc2lastmod = {url.loc: url.lastmod for url in new_urlset.url}

        remove_html_candidates: list[Path] = []
        remove_json_candidates: list[Path] = []
        remove_img_candidates: list[Path] = []

        for loc, lastmod in old_loc2lastmod.items():
            if loc not in new_loc2lastmod:
                continue
            if lastmod >= new_loc2lastmod[loc]:
                continue

            html_path = config.html_file_path(loc)
            if not html_path.exists():
                continue
            remove_html_candidates.append(html_path)

            json_path = config.json_file_path(html_path)
            if not json_path.exists():
                continue
            remove_json_candidates.append(json_path)

            recipe = Recipe.model_validate_json(json_path.read_text())
            img_path = config.img_file_path(recipe.image_url)

            if not img_path.exists():
                continue
            remove_img_candidates.append(img_path)

        remove_candidates = remove_html_candidates + remove_json_candidates + remove_img_candidates

        rich.print(f"Detected {len(remove_candidates)} outdated files.")
        if len(remove_candidates) == 0:
            return 0

        if not dry_run and Confirm.ask(
            "Are you sure you want to delete outdated files "
            "and replace sitemap with the latest version?"
        ):
            for file_path in track(
                remove_candidates, description="Removing outdated files...", transient=True
            ):
                file_path.unlink(missing_ok=True)
            rich.print(f"Removed {len(remove_candidates)} outdated files.")
            shutil.move(new_sitemap, config.sitemap_file_path())
            rich.print("Updated sitemap to the latest version.")

        return len(remove_candidates)
