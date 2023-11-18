import os
from pathlib import Path
import json
import subprocess
import psutil
import time
import threading
from selenium import webdriver

# Set file paths
folder = "../VN-tools"
LE = "Locale.Emulator.2.5.0.1/LEProc.exe"
tractor = "Textractor/x86/Textractor.exe"


html_file_path = "TexthookerOffline/TextHooker.html"
html_file_path = Path(html_file_path).resolve().as_uri()
options = webdriver.FirefoxOptions()
options.add_argument("--profile")
options.add_argument(folder + "/profile-default")


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

def run_vn(target_path):
    try:
        if target_path is not None and os.path.exists(target_path):
            print("The target path exists.")
            game_process = subprocess.Popen([LE, target_path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            print("Running: " + os.path.basename(target_path))

            # Wait for the process to fully launch, adjust time as necessary
            time.sleep(1)

            # Get the PID of the game process
            game_pid = get_pid(os.path.basename(target_path))
            textractor_process = None
            if game_pid is not None:
                if not is_process_running('Textractor.exe'):
                    textractor_process = subprocess.Popen([tractor, '-p' + str(game_pid)], stdout=subprocess.DEVNULL)
                    print("Textractor started.")
                    driver = webdriver.Firefox(options=options)
                    driver.get(html_file_path)
                    print("Texthooker opened.")
            
            while game_process.poll() is None:
                time.sleep(1)  # Sleep to reduce CPU usage
            
            if textractor_process is not None:
                textractor_process.terminate()
                print("Textractor terminated.")
                driver.quit()
                print("Texthooker closed.")
        else:
            print("The target path does not exist.")
    except Exception as e:
        print(f"Error while running VN: {e}")

def run_vn_threaded(target_path):
    # Function to run the VN in a separate thread
    vn_thread = threading.Thread(target=run_vn, args=(target_path,))
    vn_thread.start()

def main():
    json_file_path = Path(__file__).parent / "VNList.json"
    if not json_file_path.exists():
        print("No JSON file found.")
        subprocess.run(["update.bat"], cwd=Path(__file__).parent)
        print("JSON file updated.")
    
    with open(json_file_path, "r") as f:
        vnList = json.load(f)

    for i, vn in enumerate(vnList["VNList"]):
        print(f"{i + 1}. {vn['name']}")
    choice = input("Enter file number: ")

    while True:
        if choice.isdigit():
            choice = int(choice) - 1
            if choice < 0 or choice >= len(vnList["VNList"]):
                print("Invalid number.")
                choice = input("Enter file number: ")
            else:
                selected_vn = vnList["VNList"][choice]
                print(f"You've selected {selected_vn['name']} with path {selected_vn['path']}")
                run_vn_threaded(selected_vn['path'])
                break
        else:
            print("Invalid input.")
            choice = input("Enter file number: ")
    
if __name__ == "__main__":
    # Check if paths exist
    for path in [folder, LE, tractor]:
        if not os.path.exists(path):
            print(f"Path not found: {path}")
            exit()
    main()
    print("Quitting...")
