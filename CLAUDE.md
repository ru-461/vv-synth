# voicevox-playground

VOICEVOX で音声合成を試す Python プレイグラウンド。

## 触らない・コミットしない

- `voicevox_core/` — `./download` で生成（約 1.7GB）
- `download` — セットアップ用バイナリ
- `.venv/`

## 開発

```shell
uv sync --group dev
uv run ruff check . && uv run ruff format . && uv run ty check
```

- Python 3.14、`ruff` / `ty` は厳しめ（`pyproject.toml` 参照）
- 変更後は上記チェックを通す
- コミットはユーザーが明示したときのみ

## VOICEVOX

- アプリ・Engine・CORE の手順: Notion「VOICEVOXセットアップ」
- CORE 取得: `README.md` の `./download` 手順

## 方針

- 依頼範囲だけ変更する。過剰な抽象化・テスト追加は求められない限りしない。
