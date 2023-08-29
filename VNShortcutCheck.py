import os
from pathlib import Path
import sys
from pylnk3 import cli

def is_uninstaller(filename):
    """
    Check if the filename suggests it's an uninstaller.
    """
    uninstaller_keywords = ["_uninst", "_uninstall", "uninst_", "uninstall_"]
    for keyword in uninstaller_keywords:
        if keyword in filename.lower():
            return True
    return False

def create_shortcut_pylnk3(target, lnk_name):
    """
    Wrapper function to create a shortcut using pylnk3 CLI.
    """
    create_shortcut(target=target, lnk_name=lnk_name)

def create_shortcut(target, lnk_name, arguments=None, description=None, 
                    icon_file=None, icon_index=0, work_dir=None, window_mode=None):
    """
    Create a shortcut using the pylnk3 CLI.
    """
    # Build the argument list
    args = ["pylnk3", "create", target, lnk_name]
    
    if arguments:
        args.extend(["--arguments", arguments])
    if description:
        args.extend(["--description", description])
    if icon_file:
        args.extend(["--icon", icon_file])
    if icon_index:
        args.extend(["--icon-index", str(icon_index)])
    if work_dir:
        args.extend(["--workdir", work_dir])
    if window_mode:
        args.extend(["--mode", window_mode])
    
    # Set the command-line arguments and call the CLI function
    sys.argv = args
    cli()

def main():
    base_dir = Path(__file__).parent.parent  # This points to the VN folder
    deeper_folder = base_dir / "VN-collection" / "deeper"
    deeper_folder.mkdir(parents=True, exist_ok=True)  # Ensure the target folder exists

    print(f"Searching for .exe files in {base_dir} ...")

    # Search for exe files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".exe") and not is_uninstaller(file):
                full_path = Path(root) / file
                
                # Use the parent folder's name for the shortcut
                folder_name = full_path.parent.name
                shortcut_name = f"{folder_name}.lnk"
                shortcut_path = deeper_folder / shortcut_name

                # Check if the shortcut already exists
                if shortcut_path.exists():
                    print(f"Shortcut for {folder_name} already exists.") # at {shortcut_path}
                else:
                    create_shortcut_pylnk3(str(full_path), str(shortcut_path))
                    print(f"Created shortcut for {folder_name}.") # at {shortcut_path}

if __name__ == "__main__":
    main()
