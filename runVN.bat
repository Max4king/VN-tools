@echo off

set "python_script_path=D:\Games\VN Selection\VNSelLE.py"

rem Check if Python script exists
if not exist "%python_script_path%" (
    echo Python script not found: %python_script_path%
    exit /b
)

rem Run Python script
python "%python_script_path%"

exit
