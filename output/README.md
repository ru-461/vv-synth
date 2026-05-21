# output

VOICEVOX Engine で合成した音声ファイル (WAV) の成果物を格納するディレクトリ。

- CLI の既定保存先 (`uv run python main.py "テキスト"`)
- 生成ファイルは Git に含めない (`.gitignore` で除外)

## ファイル名

- `-o` / `--output` 省略時: `YYYYMMDD-HHMMSS.wav` (例: `20260521-143052.wav`)
- `-o hello.wav` 指定時: `output/hello.wav`
- `--output-dir` で別ディレクトリに変更可能
