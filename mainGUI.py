import tkinter as tk
import VNSelLE
import VNShortcutCheck
import os,json, sys
from pathlib import Path
# Set file paths
folder = Path(__file__).parent
LE = folder / "Locale.Emulator.2.5.0.1/LEProc.exe"
tractor = folder / "Textractor/x86/Textractor.exe"
json_file_path = folder / "VNList.json"
root = tk.Tk()

root.title("Visual Novel Selector")

def update_list():
    # Call the main function from VNShortcutCheck to update the list
    VNShortcutCheck.main()

    # Read the updated VNList.json file
    with open(json_file_path, "r") as file:
        vn_list = json.load(file)

    # Update the Listbox with new items
    listbox.delete(0, tk.END)
    for vn in vn_list["VNList"]:
        listbox.insert(tk.END, vn['name'])

def run_selected_item():
    # Get the selected item from the Listbox
    selected_index = listbox.curselection()
    if not selected_index:
        print("No item selected")  # Or show a warning in the GUI
        return
    selected_item = listbox.get(selected_index[0])

    with open(json_file_path, "r") as file:
        vn_list = json.load(file)
        selected_vn_path = next((vn["path"] for vn in vn_list["VNList"] if vn["name"] == selected_item), None)

    if selected_vn_path:
        # Run the selected visual novel
        VNSelLE.run_vn_threaded(selected_vn_path)
    else:
        print("Path not found for the selected item")


window_width = 500
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# root.attributes('-topmost', 1)

button_update = tk.Button(root, text="Update List", command=update_list)
button_update.pack()

listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True)

button_run = tk.Button(root, text="Run Selected", command=run_selected_item)
button_run.pack()

for path in [folder, LE, tractor]:
        if not os.path.exists(path):
            print(f"(GUI)Path not found: {path}")
            sys.exit()
if os.path.exists(json_file_path):
    with open(json_file_path, "r") as file:
        vn_list = json.load(file)
    for vn in vn_list["VNList"]:
        listbox.insert(tk.END, vn['name'])
root.mainloop()