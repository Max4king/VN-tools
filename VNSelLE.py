import os
import subprocess

# uncomment this to use the first option of finding the path using wsl
# from win32com.client import Dispatch
import psutil
import time
import pylnk3

# Set file paths
folder = "C:/Games/VN/VN-collection" # Change this your own
LE = "C:/Users/Game/Documents/Locale.Emulator.2.5.0.1/LEProc.exe" # This assume you put all the program in the Document
tractor = "C:/Users/Game/Documents/Textractor/x86/Textractor.exe"
subfolder = os.path.join(folder, "deeper")


def get_lnk_target(lnk_path):
    lnk = pylnk3.Lnk(lnk_path)
    return lnk.path


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
                normalized_filename = os.path.normpath(filename)
                files.append(os.path.join(root, normalized_filename))
    num = 0
    # Display list of files and prompt user to choose one
    for i, file in enumerate(files):
        num += 1
        print(f"{i + 1}. {os.path.basename(file)}")

    choice = input("Enter file number: ") #  Cutout feature or type 'deeper' for more options

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

    # 1. Get the target path of the chosen shortcut (WSL version)
    # shell = Dispatch('WScript.Shell')
    # shortcut = shell.CreateShortcut(files[choice])
    # target_path = shortcut.Targetpath
    # print(f"Target Path: {target_path}")
    
    # 2. Get the target path of the chosen shortcut (pylnk3 version)
    print(files[choice])
    target_path = get_lnk_target(files[choice])
    print(f"Target Path: {target_path}")
    
    # Try to check if target_path exists
    if target_path is not None and os.path.exists(target_path):
        print("The target path exists.")
        try:
            game_process = subprocess.Popen([LE, target_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        except Exception as e:
            print(f"Error while launching the game: {e}")
        # Start the chosen program with LE
        print(f"Running: {LE}, {target_path}")
        

        # Wait for the process to fully launch, adjust time as necessary
        time.sleep(3)

        # Get the PID of the game process
        game_pid = get_pid(os.path.basename(target_path))

        # If we successfully got the PID, start the tractor program and attach it to the game
        if game_pid is not None:
            if not is_process_running('textractor.exe'):
                subprocess.Popen([tractor, '-p' + str(game_pid)])
        else:
            print("Unable to find the game pid.")
            time.sleep(3)
    else:
        print("The target path does not exist.")


except Exception as e:
    print(f"An error occurred: {e}")
    input("Press Enter to close...")
