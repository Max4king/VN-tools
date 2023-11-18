import os, json
from pathlib import Path
from shutil import copyfile


def is_uninstaller(filename):
    """
    Check if the filename suggests it's an uninstaller.
    """
    uninstaller_keywords = ["_uninst", "_uninstall", "uninst_", "uninstall_", "unins000", "Textractor", "TextractorCLI"]
    for keyword in uninstaller_keywords:
        if keyword in filename.lower():
            return True
    return False

# def create_shortcut_pylnk3(target, lnk_name):
#     """
#     Wrapper function to create a shortcut using pylnk3 CLI.
#     """
#     create_shortcut(target=target, lnk_name=lnk_name)

# def create_shortcut(target, lnk_name, arguments=None, description=None, 
#                     icon_file=None, icon_index=0, work_dir=None, window_mode=None):
#     """
#     Create a shortcut using the pylnk3 CLI.
#     """
#     # Build the argument list
#     args = ["pylnk3", "create", target, lnk_name]
    
#     if arguments:
#         args.extend(["--arguments", arguments])
#     if description:
#         args.extend(["--description", description])
#     if icon_file:
#         args.extend(["--icon", icon_file])
#     if icon_index:
#         args.extend(["--icon-index", str(icon_index)])
#     if work_dir:
#         args.extend(["--workdir", work_dir])
#     if window_mode:
#         args.extend(["--mode", window_mode])
    
#     # Set the command-line arguments and call the CLI function
#     sys.argv = args
#     cli()

def find_all_exe(folder):
    files = []
    exception_folder = ["Locale.Emulator.2.5.0.1","Textractor","TexthookerOffline", "VN-tools"]
    for root, dirs, filenames in os.walk((folder)): # os.path.dirname
        if any(x in root for x in exception_folder):
            continue        
        for filename in filenames:
            if filename.endswith(".exe") and not is_uninstaller(filename):
                normalized_filename = os.path.normpath(filename)
                files.append(os.path.join(root, normalized_filename))
    return files

def main():
    os.system('chcp 65001') # Set encoding to UTF-8
    base_dir = Path(__file__).parent  # The default of mine is "D:\Games\VN\VN-tools"
    vn_folder = base_dir.parent  # The default of mine is "D:\Games\VN"
    json_file_path = base_dir / "VNList.json"
    backup_file_path = base_dir / "VNList_backup.json"
    print(f"Searching for all VN in {vn_folder} ...")
    
    exe_files_list = find_all_exe(vn_folder)

    existing_data = {
        "directory": str(vn_folder),
        "VNList": []
    }

    # Check if JSON file exists and create a backup
    if json_file_path.exists():
        copyfile(json_file_path, backup_file_path)
        print(f"Backup created at {backup_file_path}")

        # Read from existing JSON file
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)

        # Check if each exe file still exists
        for vn in existing_data["VNList"]:
            if not Path(vn["path"]).exists():
                print(f"The file {vn['path']} no longer exists.")
                existing_data["VNList"].remove(vn)

    # Add new .exe files
    for new_file in exe_files_list:
        if new_file not in [vn["path"] for vn in existing_data["VNList"]]:
            print(f"Adding new VN to the list: {new_file}")
            vn_name = Path(new_file).name.replace('.exe', '')
            vn_id = len(existing_data["VNList"]) + 1
            existing_data["VNList"].append({
                "name": vn_name,
                "id": str(vn_id),
                "path": new_file
            })

    # Write to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


    print(f"New VN have been saved in {json_file_path}")

if __name__ == "__main__":
    main()