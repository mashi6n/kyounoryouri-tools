from pathlib import Path
from urllib.parse import unquote

from pydantic import BaseModel


class WebPathConfig(BaseModel):
    html_dir: Path
    img_dir: Path
    sitemap_dir: Path
    extracted_json_dir: Path


class DatasetPathConfig(BaseModel):
    jsonl_dir: Path


class PathConfig(BaseModel):
    web: WebPathConfig
    dataset: DatasetPathConfig

    def create_all_dirs(self) -> None:
        self.web.html_dir.mkdir(parents=True, exist_ok=True)
        self.web.img_dir.mkdir(parents=True, exist_ok=True)
        self.web.sitemap_dir.mkdir(parents=True, exist_ok=True)
        self.web.extracted_json_dir.mkdir(parents=True, exist_ok=True)
        self.dataset.jsonl_dir.mkdir(parents=True, exist_ok=True)

    def sitemap_file_path(self) -> Path:
        return self.web.sitemap_dir / "recipe.xml"

    def html_file_path(self, html_url: str) -> Path:
        return self.web.html_dir / unquote(html_url.split("/")[-1])

    def json_file_path(self, html_file_path: Path) -> Path:
        return self.web.extracted_json_dir / (html_file_path.stem + ".json")

    def img_file_path(self, image_url: str) -> Path:
        return self.web.img_dir / unquote(image_url.split("/")[-1])
