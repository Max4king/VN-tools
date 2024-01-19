@echo off
chcp 65001
REM You need to chang the path here accordingly 
set "python_script_path=C:\Games\VN\VN-tools\VNSelLE.py"

rem Check if Python script exists
if not exist "%python_script_path%" (
    echo Python script not found: %python_script_path%
	timeout /t 3 /nobreak > NUL
    exit /b
)

rem Run Python script
python "%python_script_path%"

timeout /t 3 /nobreak > NUL
exit
