# cp-file-str-repdate
English version → [README.md](README.md)

このツールは、ファイル名に含まれる日付文字列を今日の日付に置き換えてコピーするシンプルなファイルコピーツールです。

INIファイルで指定した日付フォーマットに基づき、ファイル名から日付を検出・検証し、安全にコピー処理を行います。

---

■ 概要

このスクリプトは以下の処理を行います。

- コマンドライン引数で指定されたファイルを処理対象とする
- ファイル名に含まれる日付文字列を検出
- 今日の日付に置き換えたファイル名でコピーを作成
- 元ファイルを読み取り専用に設定

---

■ 機能

- argparse を使用したコマンドライン引数処理
- ファイルの存在チェック・ファイル種別チェック
- INIファイルによる日付フォーマット設定
- ファイル名中の日付文字列の正当性検証
- 今日の日付がすでに含まれている場合は処理を中止
- shutil.copy2() によるメタ情報保持コピー

---

■ 使用方法

python cp_file_str_repdate.py <処理対象ファイル>

実行例:
python cp_file_str_repdate.py memo_250101.txt

---

■ 設定ファイル（INI）

設定ファイルはスクリプトと同じフォルダに、スクリプトと同じ名前で作成します。

ファイル名例:
cp_file_str_repdate.ini

設定内容例:

[DATE]
format = %y%m%d

---

■ 日付フォーマットについて（重要）

INIファイルの format には、Python標準ライブラリ datetime.strftime() / datetime.strptime() の
日付フォーマットをそのまま使用できます。

つまり、Pythonで使用可能な日付書式指定子がすべて利用可能です。

使用例:

format = %y%m%d     → memo_250101.txt  
format = %Y%m%d     → memo_20250101.txt  
format = %Y_%m_%d   → memo_2025_01_01.txt  
format = %Y-%m-%d   → memo_2025-01-01.txt  

※ ファイル名中に、この形式と一致する日付文字列が含まれている必要があります。

---

■ 動作仕様

- 処理対象が存在しない場合、またはファイルでない場合はエラー終了します
- ファイル名に日付文字列が含まれていない場合はエラー終了します
- ファイル名の日付が今日の日付の場合、コピー処理は行われません
- コピー先は元ファイルと同じフォルダになります
- コピー完了後、元ファイルは読み取り専用属性に設定されます

---

■ エラーメッセージ例

Error: Input file not found
Error: Filename does not contain a valid date
Error: The date in the filename is today

---

■ 動作確認環境

Windows 10 / 11
Python 3.8 以上

---

■ ライセンス

MIT License

---

■ 作者

pukkunk
