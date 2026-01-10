import os
import sys
import shutil
import configparser
import re
import stat
from datetime import datetime

def get_script_dir():
    """
    Get directory where script or exe exists
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def error_exit(message: str):
    print(message)
    sys.exit(1)

def load_ini():
    script_dir = get_script_dir()
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    ini_path = os.path.join(script_dir, f"{script_name}.ini")

    if not os.path.exists(ini_path):
        error_exit(
            "Error: INI file not found.\n"
            f"Path: {ini_path}"
        )

    # Disable interpolation to allow %Y%m%d
    config = configparser.ConfigParser(interpolation=None)
    config.read(ini_path, encoding="utf-8")
    return config

def date_format_to_regex(fmt: str) -> str:
    """
    Convert strftime format to regex
    Example: %Y%m%d -> \\d{4}\\d{2}\\d{2}
    """
    regex = fmt
    regex = regex.replace("%Y", r"\d{4}")
    regex = regex.replace("%m", r"\d{2}")
    regex = regex.replace("%d", r"\d{2}")
    return regex

def main():
    # Argument check
    if len(sys.argv) < 2:
        error_exit(
            "Error: Input file is not specified.\n"
            "Usage: file_copy_tool <input_file>"
        )

    input_path = os.path.abspath(sys.argv[1])

    if not os.path.isfile(input_path):
        error_exit(
            "Error: Input file does not exist.\n"
            f"Path: {input_path}"
        )

    # Load INI
    config = load_ini()
    date_format = config["DATE"]["format"]

    file_name = os.path.basename(input_path)
    dir_path = os.path.dirname(input_path)

    # Build regex from date format
    date_regex = date_format_to_regex(date_format)

    # Search date in filename only
    m = re.search(date_regex, file_name)
    if not m:
        today_example = datetime.today().strftime(date_format)
        error_exit(
            "Error: Filename does not contain a valid date.\n"
            f"  Expected format : {date_format}\n"
            f"  Example (today) : {today_example}\n"
            f"  Example filename: report_{today_example}.txt"
        )

    old_date_str = m.group()
    today_str = datetime.today().strftime(date_format)

    # Validate date string
    try:
        datetime.strptime(old_date_str, date_format)
    except ValueError:
        error_exit(
            "Error: Invalid date in filename.\n"
            f"  Date string    : {old_date_str}\n"
            f"  Expected format: {date_format}"
        )

    # Check if date is today
    if old_date_str == today_str:
        error_exit(
            "Error: The date in the filename is today.\n"
            f"  Date in filename: {old_date_str}\n"
            f"  Today           : {today_str}\n"
            "  Please specify a file with a date other than today."
        )

    # Replace date with today
    new_file_name = file_name.replace(old_date_str, today_str)
    dst_path = os.path.join(dir_path, new_file_name)

    # Copy file (with metadata)
    shutil.copy2(input_path, dst_path)

    # Set source file to read-only
    os.chmod(input_path, stat.S_IREAD)

    print("Copy completed successfully.")
    print(f"Source      : {input_path}")
    print(f"Destination : {dst_path}")
    #print("Source file permission set to read-only.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_exit(f"Unexpected error: {e}")
