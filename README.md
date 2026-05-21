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
