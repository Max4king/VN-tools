import os
import subprocess
from win32com.client import Dispatch

# Set file paths
folder = "D:/Games/VN Selection/"
LE = "D:/Locale.Emulator.2.5.0.1/LEProc.exe"
tractor = "D:/programFiles/Textractor/x86/Textractor.exe"
subfolder = os.path.join(folder, "deeper")

# Check if paths exist
for path in [folder, LE, tractor]:
    if not os.path.exists(path):
        print(f"Path not found: {path}")
        exit()

try:
    # Get list of .lnk files in current directory
    files = []
    for root, dirs, filenames in os.walk(folder):
        if root == subfolder:
            check_subfolder = input("Do you want to check deeper folder (y/n)? ")
            if check_subfolder.lower() != 'y':
                continue
        for filename in filenames:
            if filename.endswith(".lnk"):
                files.append(os.path.join(root, filename))
    num = 0
    # Display list of files and prompt user to choose one
    for i, file in enumerate(files):
        num += 1
        print(f"{i + 1}. {os.path.basename(file)}")

    choice = int(input("Enter file number: ")) - 1
    while ( choice >= num or choice < 0):
        print("Invalid number.")
        choice = int(input("Enter file number: ")) - 1


    # Run selected file
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(files[choice])
    name = shortcut.Targetpath

    # Start the tractor program
    subprocess.Popen([tractor])

    # Start the chosen program
    subprocess.Popen([LE, name])
except Exception as e:
    print(f"An error occurred: {e}")
    input("Press Enter to close...")
