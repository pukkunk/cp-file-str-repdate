import os
import sys
import re
import shutil
import stat
import configparser
from datetime import datetime
from typing import Dict


# ============================================================
# Utility
# ============================================================

def get_script_dir() -> str:
    """
    Get directory where this script or exe exists.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def error_exit(message: str) -> None:
    print(f"Error: {message}")
    sys.exit(1)


# ============================================================
# INI handling
# ============================================================

def load_ini() -> Dict[str, str]:
    """
    Load ini file based on script filename.
    """
    script_dir: str = get_script_dir()
    script_name: str = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    ini_path: str = os.path.join(script_dir, f"{script_name}.ini")

    if not os.path.exists(ini_path):
        error_exit(f"INI file not found: {ini_path}")

    # ★ %y%m%d を扱うため interpolation 無効
    config = configparser.ConfigParser(interpolation=None)
    config.read(ini_path, encoding="utf-8")

    if "DATE" not in config:
        error_exit("Missing [DATE] section in ini file.")

    if "format" not in config["DATE"]:
        error_exit("Missing 'format' in [DATE] section.")

    return {
        "date_format": config["DATE"]["format"]
    }


# ============================================================
# Date extraction
# ============================================================

def extract_date_from_filename(filename: str, date_format: str) -> str:
    """
    Extract date string from filename using given date format.
    """
    format_map = {
        "%Y": r"\d{4}",
        "%y": r"\d{2}",
        "%m": r"\d{2}",
        "%d": r"\d{2}",
    }

    regex_pattern: str = re.escape(date_format)
    for key, value in format_map.items():
        regex_pattern = regex_pattern.replace(re.escape(key), value)

    match = re.search(regex_pattern, filename)
    if not match:
        today = datetime.today().strftime(date_format)
        error_exit(
            "Filename does not contain a valid date.\n"
            f"Expected format : {date_format}\n"
            f"Example (today) : {today}\n"
            f"Example filename: memo_{today}.txt"
        )

    date_str: str = match.group()

    # validate date
    try:
        datetime.strptime(date_str, date_format)
    except ValueError:
        error_exit(f"Invalid date value in filename: {date_str}")

    return date_str


# ============================================================
# Main
# ============================================================

def main() -> None:
    if len(sys.argv) != 2:
        error_exit("Usage: cp_file_str_repdate <input_file>")

    input_path: str = os.path.abspath(sys.argv[1])

    if not os.path.isfile(input_path):
        error_exit(f"Input file not found: {input_path}")

    # load ini
    ini: Dict[str, str] = load_ini()
    date_format: str = ini["date_format"]

    filename: str = os.path.basename(input_path)
    dir_path: str = os.path.dirname(input_path)

    # extract date
    old_date: str = extract_date_from_filename(filename, date_format)
    print(f"Detected date: {old_date}")

    today_str: str = datetime.today().strftime(date_format)

    # 今日の日付は禁止
    if old_date == today_str:
        error_exit(
            "The date in the filename is today.\n"
            f"Date in filename: {old_date}"
        )

    # create destination filename
    new_filename: str = filename.replace(old_date, today_str)
    dst_path: str = os.path.join(dir_path, new_filename)

    # copy
    shutil.copy2(input_path, dst_path)

    # set source readonly
    os.chmod(input_path, stat.S_IREAD)

    print("Copy completed successfully.")
    print(f"Source      : {input_path}")
    print(f"Destination : {dst_path}")
    #print("Source file permission set to read-only.")


if __name__ == "__main__":
    main()
