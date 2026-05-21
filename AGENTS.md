# voicevox-playground

VOICEVOX Engine を Typer CLI から呼び出す Python プレイグラウンド。詳細は `README.md` を参照。

## 構成

| パス | 役割 |
|------|------|
| `main.py` | `vv-synth` CLI (`uv run vv-synth "テキスト"`) |
| `voicevox_playground/engine_client.py` | Engine HTTP API |
| `voicevox_playground/output_paths.py` | 出力パス (`output/` 既定) |
| `samples/engine_http_sample.py` | 参考用バックアップ (直接実行用) |
| `output/` | 合成 WAV の出力先 |

## 触らない・コミットしない

- `voicevox_core/`, `download` — CORE セットアップ用 (約 1.7GB)
- `output/` 内の `*.wav` — CLI 出力
- `.venv/`, `.ruff_cache/`

## 開発

```shell
uv sync --group dev
uv run ruff check .
uv run ruff format .
uv run ty check
```

- Python 3.14、依存は `uv sync`
- `ruff` / `ty` 厳しめ (`pyproject.toml`)
- コミットはユーザー明示時のみ
- コミットメッセージ: `prefix: message` (英語ワンライン)。`feat` `fix` `docs` `chore` `update` `refactor` `test` `style`

## 実装メモ

- CLI 実行には VOICEVOX アプリ起動 (Engine `http://127.0.0.1:50021`) が必要
- 出力はカレントディレクトリの `output/` が既定。`-o` 省略時はタイムスタンプファイル名
- VOICEVOX 手順: Notion「VOICEVOXセットアップ」

## 方針

- 依頼範囲のみ変更。既存スタイルに合わせる
- 過剰な抽象化・テスト追加は求められない限りしない
