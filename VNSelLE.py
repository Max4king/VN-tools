import os
from pathlib import Path
import json
import subprocess
# uncomment this to use the first option of finding the path using wsl
# from win32com.client import Dispatch
import psutil
import time
import pylnk3
import argparse
from selenium import webdriver

"""
The 3 paths below are the only ones that need to be changed.
"""
# Set file paths
folder = "D:/Games/VN/VN-tools"
LE = "C:/Users/Game/Documents/Locale.Emulator.2.5.0.1/LEProc.exe"
tractor = "C:/Users/Game/Documents/Textractor/x86/Textractor.exe"
subfolder = os.path.join(folder, "deeper")


# firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe"
# Change to geckodriver to use selenium instead. So I could close the tab of Texthooker on browser
# Legacy way of adding extension to firefox
# clipboardAddOn = "C:/Games/VN/VN-tools/clipboard.xpi"
html_file_path = folder + "/TexthookerOffline/TextHooker.html"
options = webdriver.FirefoxOptions()
options.add_argument("--profile")
options.add_argument(folder + "/profile-default")

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


def main():
    try:
        # Get list of .lnk files in current directory
        # files = []

        # 1. Get all .lnk files in the folder
        # for root, dirs, filenames in os.walk(folder):
        #     for filename in filenames:
        #         if filename.endswith(".lnk"):
        #             normalized_filename = os.path.normpath(filename)
        #             files.append(os.path.join(root, normalized_filename))
        # Display list of files and prompt user to choose one
        # num = 0
        # for i, file in enumerate(files):
        #     num += 1
        #     file_name = os.path.basename(file).split(".")[0]
        #     print(f"{i + 1}. {file_name}")

        json_file_path = Path(__file__).parent / "VNList.json"
        if not json_file_path.exists():
            print("No JSON file found.")
            subprocess.run(["update.bat"], cwd=Path(__file__).parent)
            print("JSON file updated.")
        with open(json_file_path, "r") as f:
            vnList = json.load(f)

        for i, vn in enumerate(vnList["VNList"]):
            print(f"{i + 1}. {vn['name']}")
        choice = input("Enter file number: ") #  Cutout feature or type 'deeper' for more options
        while True:
            if choice.isdigit():
                choice = int(choice) - 1
                if choice >= len(vnList["VNList"]) or choice < 0:
                    print("Invalid number.")
                    choice = input("Enter file number: ")
                else:
                    selected_vn = vnList["VNList"][choice]
                    print(f"You've selected {selected_vn['name']} with path {selected_vn['path']}")
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
        # target_path = get_lnk_target(files[choice])
        # print(f"Target Path: {target_path}")
        # game_process = None

        # 3. Get the target path of the chosen executable
        target_path = selected_vn['path']

        # Try to check if target_path exists
        if target_path is not None and os.path.exists(target_path):
            print("The target path exists.")
            try:
                game_process = subprocess.Popen([LE, target_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            except Exception as e:
                print(f"Error while launching the game: {e}")
            # Start the chosen program
            print("Running: " + selected_vn["name"])
            

            # Wait for the process to fully launch, adjust time as necessary
            print("Waiting for the VN to launch")
            time.sleep(1)

            # Get the PID of the game process
            print("Finding pid of the VN")
            game_pid = get_pid(os.path.basename(target_path))
            textractor_process = None
            # If we successfully got the PID, start the tractor program and attach it to the game
            if game_pid is not None:
                print("VN pid found")
                if not is_process_running('Textractor.exe'):
                    print("Starting Textractor...")
                    textractor_process = subprocess.Popen([tractor, '-p' + str(game_pid)], stdout=subprocess.DEVNULL)
                    print("Textractor Started.")
                    print("Opening the Texthooker on browser...")
                    driver = webdriver.Firefox(options=options)
                    print("Browser opened.")
                    print("Loading the Texthooker on browser...")
                    driver.get(html_file_path)
                    print("Texthooker opened.")
            elif game_process is not None:
                for i in range(3):
                    print("Finding pid of the VN again...")
                    game_pid = get_pid(os.path.basename(target_path)) 
                    if game_pid is not None:
                        print("VN pid found")
                        if not is_process_running('Textractor.exe'):
                            print("Starting Textractor...")
                            textractor_process = subprocess.Popen([tractor, '-p' + str(game_pid)], stdout=subprocess.DEVNULL)
                            print("Textractor Started.")
                        break
                    else:
                        print("Unable to find the pid of the VN.")
                        time.sleep(1)
            else:
                print("Unable to find the game pid.")
                time.sleep(3)
        else:
            print("The target path does not exist.")
            
        try:
            while game_process.poll() is None:
                time.sleep(1)  # sleep for a while to reduce CPU usage
            print("Game process terminated. Terminating Textractor...")
            if textractor_process is not None:
                textractor_process.terminate()
                print("Textractor terminated.")
                driver.quit()
                print("Closing the texthooker.") 
        except Exception as e:
                print("WARNIG: Something was not close properly.")
                print("HINT: If everything except the browser was close, safely ignore the warning above")
                print("The error message:", e)
    except ImportError as e:
        print(f"An error occurred: {e}")
        input("Press Enter to close...")
    


if __name__ == "__main__":
    main()
    print("Quitting...")
