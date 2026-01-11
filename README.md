# cp-file-str-repdate
日本語版はこちら → [README.ja.md](README.ja.md)

This tool is a simple file copy utility that replaces a date string in a filename
with today's date.

Based on the date format specified in the INI file, the script detects and validates
the date in the filename and safely creates a copied file.

---

■ Overview

This script performs the following operations:

- Uses a command-line argument to specify the target file
- Detects a date string in the filename
- Replaces the date with today's date and creates a copy
- Sets the source file to read-only

---

■ Features

- Command-line argument handling using argparse
- File existence and file-type validation
- Date format configuration via INI file
- Validation of date strings in filenames
- Aborts if the filename already contains today's date
- Metadata-preserving copy using shutil.copy2()

---

■ Usage

python cp_file_str_repdate.py <input_file>

Example:
python cp_file_str_repdate.py memo_250101.txt

---

■ Configuration (INI)

The configuration file must be located in the same folder as the script
and must have the same base name as the script.

File name example:
cp_file_str_repdate.ini

Configuration example:

[DATE]
format = %y%m%d

---

■ About Date Format (Important)

The value of format in the INI file uses the same date format specification
as Python's standard library datetime.strftime() / datetime.strptime().

In other words, all date format specifiers supported by Python are available.

Examples:

format = %y%m%d     → memo_250101.txt
format = %Y%m%d     → memo_20250101.txt
format = %Y_%m_%d   → memo_2025_01_01.txt
format = %Y-%m-%d   → memo_2025-01-01.txt

Note:
The filename must contain a date string that matches the specified format.

---

■ Behavior

- Exits with an error if the input path does not exist or is not a file
- Exits with an error if no valid date string is found in the filename
- Copying is aborted if the date in the filename is already today's date
- The destination file is created in the same directory as the source file
- After copying, the source file is set to read-only

---

■ Error Message Examples

Error: Input file not found
Error: Filename does not contain a valid date
Error: The date in the filename is today

---

■ Tested Environment

Windows 10 / 11
Python 3.8 or later

---

■ License

MIT License

---

■ Author

pukkunk
