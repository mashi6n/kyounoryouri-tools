from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

import rich
from rich.panel import Panel


@dataclass(frozen=True)
class PathConfig:
    root_dir: Path

    @property
    def html_dir(self) -> Path:
        return self.root_dir / "html"

    @property
    def img_dir(self) -> Path:
        return self.root_dir / "img"

    @property
    def sitemap_dir(self) -> Path:
        return self.root_dir / "sitemap"

    @property
    def raw_recipe_json_dir(self) -> Path:
        return self.root_dir / "raw_recipe_json"

    @property
    def recipe_json_dir(self) -> Path:
        return self.root_dir / "recipe_json"

    def create_all_dirs(self) -> None:
        self.html_dir.mkdir(parents=True, exist_ok=True)
        self.img_dir.mkdir(parents=True, exist_ok=True)
        self.sitemap_dir.mkdir(parents=True, exist_ok=True)
        self.raw_recipe_json_dir.mkdir(parents=True, exist_ok=True)
        self.recipe_json_dir.mkdir(parents=True, exist_ok=True)
        rich.print("All directories have been created.\n")

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
           HTML Directory: [cyan]{self.html_dir}[/]
          Image Directory: [cyan]{self.img_dir}[/]
        Sitemap Directory: [cyan]{self.sitemap_dir}[/]
Raw Recipe JSON Directory: [cyan]{self.raw_recipe_json_dir}[/]
    Recipe JSON Directory: [cyan]{self.recipe_json_dir}[/]""",
                title="Path Configuration",
            ),
        )
        rich.print()
