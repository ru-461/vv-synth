# voicevox-playground

VOICEVOX を使った音声合成のプレイグラウンド。

## セットアップ

1. [VOICEVOX CORE](https://github.com/VOICEVOX/voicevox_core) のダウンローダを取得して実行する（プロジェクトルートで `./download` を実行すると `voicevox_core/` が展開される）
2. 詳細は Notion の「VOICEVOXセットアップ」を参照

```shell
binary=download-osx-arm64  # Intel Mac: download-osx-x64
curl -sSfL "https://github.com/VOICEVOX/voicevox_core/releases/latest/download/${binary}" -o download
chmod +x download
./download
```

## 音声合成サンプル（VOICEVOX Engine）

1. VOICEVOX アプリを起動する（Engine が `http://127.0.0.1:50021` で待ち受ける）
2. 次を実行する

```shell
uv run python main.py
```

`output.wav` に合成結果が保存される。話者 ID は `main.py` の `STYLE_ID` で変更できる（`http://127.0.0.1:50021/docs` の `/speakers` も参照）。

## 開発

```shell
uv sync --group dev
uv run ruff check .
uv run ruff format .
uv run ty check
```
