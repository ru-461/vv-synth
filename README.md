# voicevox-playground

[VOICEVOX](https://voicevox.hiroshiba.jp/) Engine を使って、Python からテキスト音声合成を試すプレイグラウンドです。

Typer 製の CLI で読み上げテキストを渡すと、合成した WAV を `output/` に保存します。HTTP API の参考実装は `samples/engine_http_sample.py` に残しています。

## 必要なもの

| 項目 | 用途 |
|------|------|
| Python 3.14+ | 実行環境 |
| [uv](https://docs.astral.sh/uv/) | 依存関係管理 |
| VOICEVOX アプリ (起動済み) | Engine API (`http://127.0.0.1:50021`) |

VOICEVOX CORE (`voicevox_core/`) は CLI では不要です。コアライブラリを試すときだけセットアップしてください。

## クイックスタート

```shell
# 依存関係のインストール
uv sync

# VOICEVOX アプリを起動してから合成
uv run python main.py "こんにちは、音声合成のテストです。"
```

成功すると `output/YYYYMMDD-HHMMSS.wav` が作成されます。

```shell
# ヘルプ
uv run python main.py --help
```

## CLI オプション

| オプション | 短縮 | 既定値 | 説明 |
|------------|------|--------|------|
| `MESSAGE` | — | (必須) | 読み上げるテキスト |
| `--output` | `-o` | 自動命名 | ファイル名またはパス |
| `--output-dir` | — | `output` | 成果物を格納するディレクトリ |
| `--speaker` | `-s` | `2` | 話者スタイル ID |
| `--engine-url` | — | `http://127.0.0.1:50021` | Engine の URL (`VOICEVOX_ENGINE_URL` 可) |

例:

```shell
# ファイル名を指定 → output/hello.wav
uv run python main.py "テストです" -o hello.wav

# 成果物ディレクトリを変更
uv run python main.py "テストです" --output-dir artifacts

# 話者を変更 (一覧は Engine の /speakers)
uv run python main.py "テストです" -s 3
```

話者スタイル ID は VOICEVOX 起動中に [http://127.0.0.1:50021/docs](http://127.0.0.1:50021/docs) の `/speakers` で確認できます。

## プロジェクト構成

```
voicevox-playground/
├── main.py                          # Typer CLI エントリーポイント
├── voicevox_playground/
│   ├── engine_client.py             # Engine HTTP API クライアント
│   └── output_paths.py              # 成果物パス (output/ など)
├── samples/
│   └── engine_http_sample.py        # 参考用 HTTP サンプル (バックアップ)
├── output/                          # 合成 WAV の成果物 (Git 除外)
│   ├── README.md
│   └── .gitkeep
├── pyproject.toml
└── uv.lock
```

## 成果物 (`output/`)

合成した WAV は **`output/`** にまとめます。生成ファイルは Git に含めません。

| 指定方法 | 保存先の例 |
|----------|------------|
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

Typer 導入前の最小 HTTP 実装です。実装の参考用に残しています。

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
| `Connection refused` | VOICEVOX アプリが起動しているか、ポート 50021 か |
| HTTP 4xx | `--speaker` のスタイル ID が環境と合っているか |
| 音声が保存されない | `--output-dir` のパス、書き込み権限 |
