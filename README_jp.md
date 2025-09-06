# KyounoRyouri Tools
このリポジトリは、日本放送協会(NHK)のウェブサイト[みんなのきょうの料理](https://www.kyounoryouri.jp/)に掲載されているレシピをダウンロードし、レシピデータを抽出するためのツールを提供します。

## 🚨 注意事項 🚨
- ***このリポジトリは非公式であり、NHKとは一切関係がありません。***
- KyounoRyouri Tools は料理レシピデータを研究目的で利用するために作られたツールです。***ダウンロードしたデータは知的財産権を考慮して適切に利用してください。***

> [!NOTE]
> "みんなのきょうの料理"は株式会社エヌエイチケイエデュケーショナルの登録商標です。

## 依存関係
- Python >= 3.10
- Pythonパッケージマネージャ（pip, uv など）

## インストール
### Python環境にインストール
pip
```bash
pip install git+https://github.com/mashi6n/kyounoryouri-tools.git
kyounoryouri-tools --help
```

uv
```bash
uv add git+https://github.com/mashi6n/kyounoryouri-tools.git
uv run kyounoryouri-tools --help
```

### コマンドラインツールとしてインストール
pipx
```bash
pipx install git+https://github.com/mashi6n/kyounoryouri-tools.git
kyounoryouri-tools --help
```

uvx
```bash
uv tool install git+https://github.com/mashi6n/kyounoryouri-tools.git
uvx kyounoryouri-tools --help
```

## 使い方
### `kyounoryouri-tools init`
```bash
kyounoryouri-tools init
```
レシピのダウンロードに必要な情報（サイトマップ）やディレクトリを初期化します。

**オプション引数**
- `--data-dir`: データを保存するディレクトリのパス。このディレクトリをルートディレクトリとして様々なデータを保存する。デフォルトは`./data`。
- `--overwrite`: このフラグを立てると既存のデータを上書きする。デフォルトは`False`。
- `--sitemap-url`: ダウンロードするレシピのサイトマップURL。デフォルトは`https://www.kyounoryouri.jp/sitemap/recipe.xml`。レシピサイトそのものが変更された場合にのみ変更する。

### `kyounoryouri-tools download`
```bash
kyounoryouri-tools download
```
レシピのHTMLファイルと画像をダウンロードし、HTMLファイルからレシピデータを抽出します。
- HTMLファイル内の構造化データを保ったJSONファイルと、一般的なレシピデータとして用いられるJSONファイルの2種類のJSONファイルを抽出します。
- 既にダウンロードされているデータをスキップし、未ダウンロードのデータのみをダウンロードします。
- サイトマップが存在する限り、同じコマンドを実行することでダウンロードを再開できます。

**オプション引数**
- `--data-dir`: データを保存するディレクトリのパス。このディレクトリをルートディレクトリとして様々なデータを保存する。デフォルトは`./data`。

> [!WARNING]
> `download`コマンドは約25000のHTMLファイルとその同数の画像をダウンロードするため、完了までに約半日かかります。
> ウェブサイトへの過度な負荷を避けるため、***既定のダウンロード間隔を変更しないでください。***

### `kyounoryouri-tools update`
```bash
kyounoryouri-tools update
```
サイトマップを更新し古くなったファイルを削除します。
- サイトマップには各HTMLファイルの最終更新日時が含まれているため、サイトマップを比較することで古くなったHTMLファイルを特定し、関連する画像やJSONファイルも含めて削除します。
- アップデートを行った後に再度`download`コマンドを実行することで、outdatedなデータを更新します。
- データセットの状態を変更したくない場合はこのコマンドを実行しないでください。

**オプション引数**
- `--data-dir`: データを保存するディレクトリのパス。このディレクトリをルートディレクトリとして様々なデータを保存する。デフォルトは`./data`。
- `--sitemap-url`: ダウンロードするレシピのサイトマップURL。デフォルトは`https://www.kyounoryouri.jp/sitemaps/recipe.xml`。レシピサイトそのものが変更された場合にのみ変更する。
- `--overwrite`: このフラグを立てると既存のサイトマップを上書きし、古くなったファイルを削除する。デフォルトは`False`。

## ディレクトリ構成
ダウンロードしたデータは以下のようなディレクトリ構成で保存されます。`DATASET_ROOT`は`--data-dir`で指定したディレクトリです。
```
DATASET_ROOT/
│
├── sitemap/
│   └── recipe.xml    # サイトマップファイル
│
├── html/             # HTMLファイル
│   └── XXX.html      # URLの末尾に対応するファイル名
│
├── img/              # レシピの完成画像
│   └── YYY.jpg       # HTMLファイルに記載された画像URLの末尾に対応するファイル名 
│
├── raw_recipe_json/  # HTMLファイルから抽出された構造化データを保ったJSONファイル
│   └── XXX.json      # ファイル名は対応するHTMLファイル名と同じ
│
└── recipe_json/      # HTMLファイルから抽出された一般的なレシピデータを保ったJSONファイル
    └── XXX.json      # ファイル名は対応するHTMLファイル名と同じ
```

## データ構造
### Raw Recipe
HTMLファイルから抽出された構造化データを保ったJSONファイルのデータ構造は[`raw_recipe.py`](./src/kyounoryouri_tools/models/raw_recipe.py)に定義されています。

`DATASET_ROOT/raw_recipe_json`にあるレシピデータはこのデータモデルを用いて次のようにパースすることができます。
```python
from kyounoryouri_tools.models import RawRecipe
from pathlib import Path

p = Path("data/raw_recipe_json/XXX.json")
raw_recipe = RawRecipe.model_validate_json(p.read_text())
print(raw_recipe.title)
```

### Recipe
一般的なレシピデータを持つJSONファイルのデータ構造は、[`recipe.py`](./src/kyounoryouri_tools/models/recipe.py)に定義されています。

`DATASET_ROOT/recipe_json`にあるレシピデータはこのデータモデルを用いて次のようにパースすることができます。
```python
from kyounoryouri_tools.models import Recipe
from pathlib import Path

p = Path("data/recipe_json/XXX.json")
recipe = Recipe.model_validate_json(p.read_text())
print(recipe.title)
```
