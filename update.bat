@echo off
chcp 65001
set "python_update_path=VNShortcutCheck.py"
if not exist "%python_update_path%" (
    echo Python script not found: %python_update_path%
	timeout /t 3 /nobreak > NUL
    exit /b
)


rem Run Python script
echo Updating the VN list....
python "%python_update_path%"
echo Update Complete

timeout /t 3 /nobreak > NUL
exit
