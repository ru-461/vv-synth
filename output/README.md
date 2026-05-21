# output

`vv-synth` が合成した WAV の既定保存ディレクトリ。

- コマンドを実行したディレクトリの `output/` に書き出す (既定)
- 生成ファイルは Git に含めない (`.gitignore` で除外)

## ファイル名

- `-o` / `--output` 省略時: `YYYYMMDD-HHMMSS.wav` (例: `20260521-143052.wav`)
- `-o hello.wav` 指定時: `output/hello.wav`
- `--output-dir` で別ディレクトリに変更可能
