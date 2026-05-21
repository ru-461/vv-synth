# vv-synth — Claude Code 向けガイド

このファイルは **Claude Code** 用の要約です。詳細なメンテナンス手順・Mermaid 図は [`README.md`](README.md)、Cursor 等との共通ルールは [`AGENTS.md`](AGENTS.md) を正本としてください。

## 何をするプロジェクトか

`vv-synth` は VOICEVOX Engine（HTTP, 既定 `:50021`）でテキストを WAV 化する Typer CLI。パッケージ名 `vv-synth`、ライブラリ `vv_synth/`、エントリ `main:main`。

## VOICEVOX Engine（Docker）

```shell
docker pull voicevox/voicevox_engine:cpu-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
```

別ターミナルで `curl -sSf http://127.0.0.1:50021/version` → 成功後に `uv run vv-synth "確認"`。

## ファイルマップ

```
main.py                   → CLI のみ（ビジネスロジックは vv_synth へ）
vv_synth/engine_client.py → audio_query → speed → synthesis → save
vv_synth/output_paths.py  → output/ と -o のパス解決
skills/vv-synth/            → 他プロジェクト向け Agent Skill（gh skill install）
skills/vv-synth-dev/        → 本リポ開発用 Skill
```

## 変更時の最短ルート

1. 該当 Python を編集（上記マップ参照）
2. `uv run ruff check . && uv run ruff format . && uv run ty check`
3. Docker で Engine 起動 → `uv run vv-synth "確認"`
4. **モジュール境界・Engine API・CLI フローが変わったら** README の Mermaid 2 枚を更新（README「グラフ (Mermaid) の更新」参照）
5. `AGENTS.md` と Agent Skills（`skills/`、`.cursor/skills/vv-synth-dev/`）を必要なら同期
6. ユーザーがコミットを依頼したときだけ commit（`prefix: message` 英語）

## 禁止・注意

- `voicevox_core/`, `download`, `output/*.wav` をコミットしない
- `samples/` は参考用。機能追加をここに書かず `vv_synth/` + `main.py` へ
- スコープ外のリファクタ・テスト大量追加はしない
- `--help` は英語のまま維持
- 合成エラーは英語 1 行（トレースバックをユーザーに見せない）

## コマンド

```shell
uv sync --group dev
uv run vv-synth --help
uv tool install --editable .   # グローバル vv-synth
```

Engine 手順の正本: README [VOICEVOX Engine の起動 (Docker)](README.md#voicevox-engine-の起動-docker)

Claude Code へ Skill を入れる: `gh skill install OWNER/vv-synth vv-synth --scope user --agent claude-code`（詳細は [`skills/README.md`](skills/README.md)）
