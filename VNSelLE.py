import os
import subprocess
from win32com.client import Dispatch
import psutil
import time

# Set file paths
folder = "C:/VN-collection" # A folder that contains only the shortcut to the vn exe and this python program
LE = "C:/Locale.Emulator.2.5.0.1/LEProc.exe"
tractor = "C:/Textractor/x86/Textractor.exe"
subfolder = os.path.join(folder, "deeper")

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def get_pid(process_name):
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

# Check if paths exist
for path in [folder, LE, tractor]:
    if not os.path.exists(path):
        print(f"Path not found: {path}")
        exit()

try:
    # Get list of .lnk files in current directory
    files = []
    for root, dirs, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(".lnk"):
                files.append(os.path.join(root, filename))
    num = 0
    # Display list of files and prompt user to choose one
    for i, file in enumerate(files):
        num += 1
        print(f"{i + 1}. {os.path.basename(file)}")

    choice = input("Enter file number or type 'deeper' for more options: ")
    while True:
        if choice.lower() == 'deeper':
            for i, file in enumerate(files):
                if subfolder in file:
                    print(f"{i + 1}. {os.path.basename(file)}")
            choice = input("Enter file number: ")
        elif choice.isdigit():
            choice = int(choice) - 1
            if (choice >= num or choice < 0):
                print("Invalid number.")
                choice = input("Enter file number: ")
            else:
                break
        else:
            print("Invalid input.")
            choice = input("Enter file number: ")

    # Get the target path of the chosen shortcut
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(files[choice])
    target_path = shortcut.Targetpath
    print(target_path);

    # Start the chosen program with LE
    game_process = subprocess.Popen([LE, target_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

    # Wait for the process to fully launch, adjust time as necessary
    time.sleep(3)

    # Get the PID of the game process
    game_pid = get_pid(os.path.basename(target_path))

    # If we successfully got the PID, start the tractor program and attach it to the game
    if game_pid is not None:
        if not is_process_running('textractor.exe'):
            subprocess.Popen([tractor, '-p' + str(game_pid)])

except Exception as e:
    print(f"An error occurred: {e}")
    input("Press Enter to close...")
