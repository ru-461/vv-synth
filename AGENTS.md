# vv-synth — AI コーディングエージェント向けガイド

VOICEVOX Engine 向け CLI **`vv-synth`** のリポジトリ。利用者向け説明は [`README.md`](README.md)、アーキテクチャ図とメンテナンス手順も同ファイルにあります。

## プロジェクトの目的

- テキストを VOICEVOX Engine で合成し、WAV をローカルに保存する
- 実装の中心は **`vv_synth/engine_client.py`**（HTTP）と **`main.py`**（Typer CLI）
- VOICEVOX CORE (`voicevox_core/`) は本 CLI では使わない

## クイックリファレンス

```shell
uv sync --group dev
uv run ruff check . && uv run ruff format . && uv run ty check
uv run vv-synth "テスト"    # 要 VOICEVOX 起動
```

グローバル CLI: `uv tool install --editable .` → コマンド `vv-synth`

## 構成と責務

| パス | 責務 | 変更時に見るドキュメント |
|------|------|--------------------------|
| `main.py` | Typer CLI、オプション、ログ、`main:main` エントリ | README 使い方、Mermaid シーケンス (`main.py` ノード) |
| `vv_synth/engine_client.py` | `/audio_query`, `/synthesis`, 話速, エラー変換 | README Mermaid 両方、`engine_client` 矢印 |
| `vv_synth/output_paths.py` | `output/`、`-o`、タイムスタンプファイル名 | README 出力先、`output/README.md` |
| `samples/engine_http_sample.py` | 参考用（CLI 非連携） | 依頼がなければ触らない |
| `pyproject.toml` | パッケージ名 `vv-synth`、`[project.scripts]` | README インストール手順 |
| `output/` | 生成 WAV（Git 除外） | コミットしない |

## 処理フロー（実装の正）

1. `main.synth` が `resolve_output_file()` で保存パスを決定
2. `synthesize_text_to_file()` が Engine に接続
3. `POST /audio_query` → `apply_speed_scale()` → `POST /synthesis` → `save_wav()`

図の正本: README の **コンポーネント構成** / **合成処理の流れ**（Mermaid）。フローを変えたら **必ず README の Mermaid を更新**（手順は README「グラフ (Mermaid) の更新」）。

## 変更プレイブック

| 依頼の例 | 編集 | 必須の確認 |
|----------|------|------------|
| 新しい CLI フラグ | `main.py` | `uv run vv-synth --help`、README オプション表 |
| 出力先ルール | `vv_synth/output_paths.py` | 手動で `-o` / `--output-dir` を試す |
| Engine 連携・話速 | `vv_synth/engine_client.py` | 合成成功、README Mermaid 更新 |
| コマンド名変更 | `pyproject.toml` scripts + `main.py` `Typer(name=...)` | `uv tool install --editable .` |
| 依存追加 | `pyproject.toml` | `uv lock` |

## 触らない・コミットしない

- `voicevox_core/`, `download` — 大容量 CORE セットアップ
- `output/**/*.wav` — CLI 生成物
- `.venv/`, `.ruff_cache/`, `dist/`, `build/`

## 品質・スタイル

- Python 3.14、`uv sync --group dev`
- `ruff` / `ty`: `pyproject.toml` で厳しめ（`select = ["ALL"]` など）
- 相対 import 禁止（`ban-relative-imports = "all"`）
- `--help` 向け docstring に `Raises: typer.Exit` は書かない（`DOC501` 回避のため `main.py` で ignore）
- CLI `--help` 文言は **英語**（利用者向け README 本文は日本語可）

## コミット・スコープ

- **コミットはユーザーが明示したときのみ**
- メッセージ: `prefix: message`（英語ワンライン）— `feat` `fix` `docs` `chore` `update` `refactor` `test` `style`
- 依頼範囲のみ変更。不要な抽象化・テスト追加は求められない限りしない
- 既存の命名・モジュール分割に合わせる

## 外部依存・検証

- 実行時: VOICEVOX アプリ起動 → Engine `http://127.0.0.1:50021`（`VOICEVOX_ENGINE_URL` で上書き可）
- 話者 ID 既定 `2`（環境で異なる場合あり）
- 手順詳細: Notion「VOICEVOXセットアップ」
- Engine 未起動時は `EngineClientError` → exit code 1

## ドキュメント同期（エージェント用チェックリスト）

実装を変えたら、該当項目だけでよいので同期する。

1. README Mermaid（コンポーネント / シーケンス）— 境界・API・モジュール名が変わったとき
2. README オプション表 — CLI フラグを変えたとき
3. 本ファイル (`AGENTS.md`) と `CLAUDE.md` の構成表
4. `output/README.md` — 出力規則を変えたとき
