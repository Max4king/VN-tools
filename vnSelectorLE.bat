@echo off
setlocal enabledelayedexpansion

rem %~dp0 for current directory that this batch is at
rem Change it to your own directory where you store your VN shortcut
set "folder=%~dp0"
rem Change this is Your own location. This is the Default One
rem C:\Program Files\Locale.Emulator.2.5.0.1\LEProc.exe
set "LE=C:\Program Files\Locale.Emulator.2.5.0.1\LEProc.exe"
rem Get list of .lnk files in current directory
set "count=0"
for %%f in ("%folder%*.lnk") do (
    set /a "count+=1"
    set "file[!count!]=%%~nf"
)

rem Display list of files and prompt user to choose one
echo Please choose which file to run:
for /l %%i in (1,1,%count%) do (
    set "name=!file[%%i]!"
    echo %%i. !name!
)
set /p choice=Enter file number:

rem Run selected file
set "name=!file[%choice%]!.lnk"
if exist "!name!" (
	for /f "usebackq delims=" %%P in (`powershell.exe -c "(New-Object -ComObject WScript.Shell).CreateShortcut('%name%').TargetPath"`) do set "name=%%P"
) else (
    echo Invalid choice
    exit /b 1
)
rem Change the PATH to your own directory
echo "!name!"

start "" "!LE!" "!name!" && start cmd /c "echo  echo Enjoy Your VN :D && echo  && timeout /t 3 > nul" && exit

rem extra exit just incase.
exit
