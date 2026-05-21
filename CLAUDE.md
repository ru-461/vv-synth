# voicevox-playground

VOICEVOX Engine を Typer CLI から呼び出す Python プレイグラウンド。詳細は `README.md` を参照。

## 構成

| パス | 役割 |
|------|------|
| `main.py` | Typer CLI (`uv run python main.py "テキスト"`) |
| `voicevox_playground/engine_client.py` | Engine HTTP API |
| `voicevox_playground/output_paths.py` | 成果物パス (`output/` 既定) |
| `samples/engine_http_sample.py` | 参考用バックアップ (直接実行用) |
| `output/` | 合成 WAV の成果物 |

## 触らない・コミットしない

- `voicevox_core/`, `download` — CORE セットアップ用 (約 1.7GB)
- `output/` 内の `*.wav` — CLI 成果物
- `.venv/`, `.ruff_cache/`

## 開発

```shell
uv sync --group dev
uv run ruff check . && uv run ruff format . && uv run ty check
```

- Python 3.14、依存は `uv sync`
- `ruff` / `ty` 厳しめ (`pyproject.toml`)
- コミットはユーザー明示時のみ
- コミットメッセージ: `prefix: message` (英語ワンライン)。`feat` `fix` `docs` `chore` `update` `refactor` `test` `style`

## 実装メモ

- CLI 実行には VOICEVOX アプリ起動 (Engine `http://127.0.0.1:50021`) が必要
- 成果物は `output/` に集約。`-o` 省略時はタイムスタンプファイル名
- VOICEVOX 手順: Notion「VOICEVOXセットアップ」

## 方針

- 依頼範囲のみ変更。過剰な抽象化・テスト追加は求められない限りしない
