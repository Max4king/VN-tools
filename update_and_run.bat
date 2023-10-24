@echo off
chcp 65001
set "python_update_path=D:\Games\VN\VN-tools\VNShortcutCheck.py"
set "python_script_path=D:\Games\VN\VN-tools\VNSelLE.py"
rem Check if Python script exists
if not exist "%python_script_path%" (
    echo Python script not found: %python_script_path%
	timeout /t 3 /nobreak > NUL
    exit /b
)
if not exist "%python_update_path%" (
    echo Python script not found: %python_update_path%
	timeout /t 3 /nobreak > NUL
    exit /b
)


rem Run Python script
echo Updating the VN list....
python "%python_update_path%"
echo Update Complete
echo Starting.....
python "%python_script_path%"

timeout /t 3 /nobreak > NUL
exit
