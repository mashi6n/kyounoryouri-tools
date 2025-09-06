# KyounoRyouri Tools

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](./LICENSE)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![ci](https://github.com/mashi6n/kyounoryouri-tools/actions/workflows/ci.yaml/badge.svg)](https://github.com/mashi6n/kyounoryouri-tools/actions/workflows/ci.yaml)

[🇯🇵 Japanese](./README_ja.md)

KyounoRyouri Tools provides utilities to download and extract recipe data from [Minna no Kyō no Ryōri](https://www.kyounoryouri.jp/), a cooking recipe website operated by Japan Broadcasting Corporation (NHK).


## 🚨 Disclaimer

- ***This project is unofficial and not affiliated with NHK.***
- KyounoRyouri Tools is designed for ***research purposes only***. Please ensure that any downloaded data is used responsibly and with respect to intellectual property rights.

> [!NOTE]  
> “Minna no Kyō no Ryōri” is a registered trademark of NHK Educational Corporation.

## Requirements

- Python ≥ 3.10  
- Python package manager (e.g., `pip`, `uv`)

## Installation

### Install into an existing Python environment

**pip**
```bash
pip install git+https://github.com/mashi6n/kyounoryouri-tools.git
kyounoryouri-tools --help
```

**uv**
```bash
uv add git+https://github.com/mashi6n/kyounoryouri-tools.git
uv run kyounoryouri-tools --help
```

### Install as a standalone CLI tool

**pipx**
```bash
pipx install git+https://github.com/mashi6n/kyounoryouri-tools.git
kyounoryouri-tools --help
```

**uvx**
```bash
uv tool install git+https://github.com/mashi6n/kyounoryouri-tools.git
uvx kyounoryouri-tools --help
```

## Usage

### Initialize: `kyounoryouri-tools init`
```bash
kyounoryouri-tools init
```
Sets up the sitemap and directory structure required for downloading recipes.

**Options**
- `--data-dir` : Root directory for storing data (default: `./data`)  
- `--overwrite` : Overwrite existing data (default: `False`)  
- `--sitemap-url` : Sitemap URL for recipes (default: `https://www.kyounoryouri.jp/sitemap/recipe.xml`)  

### Download recipes: `kyounoryouri-tools download`
```bash
kyounoryouri-tools download
```
Downloads HTML files and recipe images, then extracts JSON data.  

- Produces two JSON formats:  
  - **Raw structured JSON** (faithful to the HTML structure)  
  - **Normalized recipe JSON** (commonly used recipe format)  
- Skips already downloaded data and resumes from where it left off.  
- Works incrementally as long as the sitemap is available.  

**Options**
- `--data-dir` : Root directory for storing data (default: `./data`)  

> [!WARNING]  
> This will download ~25,000 HTML files and the same number of images.  
> The process may take **half a day or more**.  
> To avoid excessive load on the website, ***do not modify the default download interval.***

### Update dataset: `kyounoryouri-tools update`
```bash
kyounoryouri-tools update
```
Updates the sitemap and removes outdated files.

- Outdated HTML files are identified via sitemap `lastmod` timestamps.  
- Removes old HTML files along with related images and JSON files.  
- After updating, run `download` again to fetch the latest data.  
- Skip this command if you need a frozen dataset version.  

**Options**
- `--data-dir` : Root directory for storing data (default: `./data`)  
- `--sitemap-url` : Sitemap URL (default: `https://www.kyounoryouri.jp/sitemaps/recipe.xml`)  
- `--overwrite` : Replace existing sitemap and remove outdated files (default: `False`)  

## Directory Layout

Data is stored in the following structure (with `DATASET_ROOT` = `--data-dir`):

```
DATASET_ROOT/
│
├── sitemap/
│   └── recipe.xml    # Sitemap XML file
│
├── html/             # Downloaded HTML files
│   └── XXX.html
│
├── img/              # Recipe images
│   └── YYY.jpg
│
├── raw_recipe_json/  # JSON preserving original HTML structure
│   └── XXX.json
│
└── recipe_json/      # Normalized recipe JSON
    └── XXX.json
```

## Data Models

### Raw Recipe
Structured JSON extracted from HTML. Defined in [`raw_recipe.py`](./src/kyounoryouri_tools/models/raw_recipe.py).

```python
from kyounoryouri_tools.models import RawRecipe
from pathlib import Path

p = Path("data/raw_recipe_json/XXX.json")
raw_recipe = RawRecipe.model_validate_json(p.read_text())
print(raw_recipe.title)
```

### Recipe
Normalized recipe JSON format. Defined in [`recipe.py`](./src/kyounoryouri_tools/models/recipe.py).

```python
from kyounoryouri_tools.models import Recipe
from pathlib import Path

p = Path("data/recipe_json/XXX.json")
recipe = Recipe.model_validate_json(p.read_text())
print(recipe.title)
```

## Contributing

Contributions are welcome!
Please open issues or pull requests on GitHub.

## Citation
If you find KyounoRyouri Tools useful in your research, we would appreciate it if you could cite the following paper:

(To be updated upon publication)
```bibtex
@misc{toyooka2025highlycleanrecipedataset,
      title={A Highly Clean Recipe Dataset with Ingredient States Annotation for State Probing Task}, 
      author={Mashiro Toyooka and Kiyoharu Aizawa and Yoko Yamakata},
      year={2025},
      eprint={2507.17232},
      archivePrefix={arXiv},
      primaryClass={cs.MM},
      url={https://arxiv.org/abs/2507.17232}, 
}
```
