# voicevox-playground

[VOICEVOX](https://voicevox.hiroshiba.jp/) Engine を使って、Python からテキスト音声合成を試すプレイグラウンドです。

`vv-synth` コマンドに読み上げテキストを渡すと、合成した WAV を保存します。HTTP API の参考実装は `samples/engine_http_sample.py` に残しています。

## 必要なもの

| 項目 | 用途 |
|------|------|
| Python 3.14+ | 実行環境 |
| [uv](https://docs.astral.sh/uv/) | 依存関係管理 |
| VOICEVOX アプリ (起動済み) | Engine API (`http://127.0.0.1:50021`) |

VOICEVOX CORE (`voicevox_core/`) は CLI では不要です。コアライブラリを試すときだけセットアップしてください。

## クイックスタート

```shell
uv sync
uv run vv-synth --help
```

VOICEVOX アプリを起動してから:

```shell
vv-synth "こんにちは、音声合成のテストです。"
```

`vv-synth` が PATH にない場合は、先に [グローバル CLI のインストール](#グローバル-cli-のインストール) を行うか、プロジェクト内では `uv run vv-synth` を使います。

成功すると、実行したディレクトリの `output/YYYYMMDD-HHMMSS.wav` が作成されます。

## グローバル CLI のインストール

どのディレクトリからでも `vv-synth` を使うには、プロジェクト直下で一度だけ次を実行します。ソースを編集した変更は `--editable` により再インストールなしで反映されます。

```shell
uv tool install --editable .
```

`~/.local/bin` が PATH に入っていない場合:

```shell
uv tool update-shell
# または
export PATH="$HOME/.local/bin:$PATH"
```

アンインストール:

```shell
uv tool uninstall voicevox-playground
```

## 使い方

```shell
vv-synth MESSAGE [OPTIONS]
```

### オプション

| オプション | 短縮 | 既定値 | 説明 |
|------------|------|--------|------|
| `MESSAGE` | — | (必須) | 読み上げるテキスト |
| `--output` | `-o` | 自動命名 | 出力 WAV のファイル名またはパス |
| `--output-dir` | — | `output` | WAV を保存するディレクトリ |
| `--speaker` | `-s` | `2` | 話者スタイル ID |
| `--speed` | — | `1.0` | 話速 (`1.0` が標準。大きいほど速い) |
| `--engine-url` | — | `http://127.0.0.1:50021` | Engine の URL (`VOICEVOX_ENGINE_URL` でも指定可) |

### 例

```shell
# ファイル名を指定 → output/hello.wav
vv-synth "テストです" -o hello.wav

# 保存ディレクトリを変更
vv-synth "テストです" --output-dir artifacts

# 話者を変更 (一覧は Engine GET /speakers)
vv-synth "テストです" -s 3

# 話速を 1.5 倍に
vv-synth "テストです" --speed 1.5
```

話者スタイル ID は VOICEVOX 起動中に [http://127.0.0.1:50021/docs](http://127.0.0.1:50021/docs) の `/speakers` で確認できます。

## プロジェクト構成

```
voicevox-playground/
├── main.py                          # vv-synth のエントリーポイント
├── voicevox_playground/
│   ├── engine_client.py             # Engine HTTP API クライアント
│   └── output_paths.py              # 出力パス (output/ など)
├── samples/
│   └── engine_http_sample.py        # 参考用 HTTP サンプル
├── output/                          # 合成 WAV の出力先 (Git 除外)
│   ├── README.md
│   └── .gitkeep
├── pyproject.toml
└── uv.lock
```

## 出力先 (`output/`)

合成した WAV は、**コマンドを実行したディレクトリ**の `output/` に保存するのが既定です。生成ファイルは Git に含めません。

| 指定 | 保存先の例 |
|------|------------|
| `-o` 省略 | `output/20260521-143052.wav` |
| `-o hello.wav` | `output/hello.wav` |
| `-o path/to/a.wav` | 指定パスそのまま |
| `--output-dir artifacts` | `artifacts/...` |

詳細は [output/README.md](output/README.md) を参照してください。

## VOICEVOX CORE のセットアップ (任意)

コアライブラリ連携を試す場合のみ、プロジェクトルートでダウンローダを実行します。

```shell
binary=download-osx-arm64  # Intel Mac: download-osx-x64
curl -sSfL "https://github.com/VOICEVOX/voicevox_core/releases/latest/download/${binary}" -o download
chmod +x download
./download   # voicevox_core/ が展開される
```

アプリ・Engine・CORE の手順まとめ: Notion「VOICEVOXセットアップ」

## 参考用サンプル

Typer 導入前の最小 HTTP 実装です。

```shell
uv run python samples/engine_http_sample.py
```

`output/sample.wav` に保存します (要 VOICEVOX 起動)。

## 開発

```shell
uv sync --group dev
uv run ruff check .
uv run ruff format .
uv run ty check
```

- `ruff` / `ty` は厳しめ (`pyproject.toml` 参照)
- コミットメッセージ: 英語ワンライン、`prefix: message` (例: `feat: add CLI option`)

## トラブルシュート

| 症状 | 確認すること |
|------|----------------|
| `command not found: vv-synth` | `uv tool install --editable .` と PATH (`~/.local/bin`) |
| `Connection refused` | VOICEVOX アプリが起動しているか、ポート 50021 か |
| HTTP 4xx | `--speaker` のスタイル ID が環境と合っているか |
| 音声が保存されない | カレントディレクトリ、`--output-dir`、書き込み権限 |
