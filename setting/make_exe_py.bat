@echo off
if not exist venv (
    python -m venv venv
)
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec
call %~dps0%venv\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pyinstaller %~dps0%cp_file_str_repdate.py --onefile
pause
