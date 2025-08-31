from pathlib import Path
from urllib.parse import unquote

import rich
from pydantic import BaseModel
from rich.panel import Panel


class PathConfig(BaseModel):
    html_dir: Path
    img_dir: Path
    sitemap_dir: Path
    raw_recipe_json_dir: Path
    recipe_json_dir: Path

    def create_all_dirs(self) -> None:
        self.html_dir.mkdir(parents=True, exist_ok=True)
        self.img_dir.mkdir(parents=True, exist_ok=True)
        self.sitemap_dir.mkdir(parents=True, exist_ok=True)
        self.raw_recipe_json_dir.mkdir(parents=True, exist_ok=True)
        self.recipe_json_dir.mkdir(parents=True, exist_ok=True)

    def exist_all(self) -> bool:
        return (
            self.html_dir.exists()
            and self.img_dir.exists()
            and self.sitemap_dir.exists()
            and self.raw_recipe_json_dir.exists()
            and self.recipe_json_dir.exists()
        )

    def sitemap_file_path(self) -> Path:
        return self.sitemap_dir / "recipe.xml"

    def html_file_path(self, html_url: str) -> Path:
        return self.html_dir / unquote(html_url.split("/")[-1])

    def raw_recipe_json_file_path(self, html_file_path: Path) -> Path:
        return self.raw_recipe_json_dir / (html_file_path.stem + ".json")

    def recipe_json_file_path(self, html_file_path: Path) -> Path:
        return self.recipe_json_dir / (html_file_path.stem + ".json")

    def img_file_path(self, image_url: str) -> Path:
        return self.img_dir / unquote(image_url.split("/")[-1])

    def print(self) -> None:
        rich.print(
            Panel.fit(
                f"""\
HTML Directory: [yellow]{self.html_dir}[/]
Image Directory: [yellow]{self.img_dir}[/]
Sitemap Directory: [yellow]{self.sitemap_dir}[/]
Raw Recipe JSON Directory: [yellow]{self.raw_recipe_json_dir}[/]
Recipe JSON Directory: [yellow]{self.recipe_json_dir}[/]""",
                title="Path Configuration",
            ),
        )
