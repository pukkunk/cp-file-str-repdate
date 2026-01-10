echo off
SET VER=100
call :PY2
call :SETTING
echo %~N0%~X0 Version=%VER%

if "%~1"=="" goto error1
REM %~dps1 = %1変数の値をフルパスで扱う際のドライブ+パス名になる。%変数の値を短縮形（dir /xと同等）に変換したもの。
if not exist "%~dps1" goto error2

rem ファイル情報が"ダブルクォーテーション"で括られた場合に"ダブルクォーテーション"を削除。
rem path情報に半角空白が含まれる場合に対応し、変数ARGに連結する処理を実施。
set "ARG="
:loop
if "%~1"=="" goto run
call set "ARG=%ARG%%~1"
shift
goto loop
:RUN
%PY% "%TOOL1%" "%ARG%"
IF ERRORLEVEL 2 GOTO error3
goto end

:PY1
	REM python実行環境なし
	SET EXT=.exe
	SET PY=
exit /b 0
:PY2
	REM python実行環境あり
	SET EXT=.py
	if defined DEBUG SET PY=python -O
	if not defined DEBUG SET PY=python
exit /b 0

:SETTING
	rem echo call :SETTING
    REM perl/pythonスクリプトがバッチファイルフォルダ + "\setting"フォルダに配置
    SET SCRIPT1=setting\cp_file_str_repdate%EXT%
    SET TOOL1=%~dps0%SCRIPT1%
exit /b 0

:error4
echo --  python script error detect
goto end
:error3
echo --  python script error detect
goto end
:error2
echo --  input file error. There is not %1
goto end
:error1
ECHO argument error. There is NOT %1 file.

:END
REM 環境変数%NOTPAUSE%が定義のときにPAUSEを実施しない
if not defined NOTPAUSE PAUSE
