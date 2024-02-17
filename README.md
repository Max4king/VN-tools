# VN-tools

This is where I plan to make my own tools to make playing vn easier.

P.S. It could also be used as a quick installer.

## No more update
This tool will no longer be updated. Since I have manage to setup VN in linux, I no longer use Window for anything else now. I may rewrite the script for linux in the future.

## What can this do?
This program helps you run the VN quicker. It runs the Locale Emulator and Textractor within one step. It can also help you organize your VN and japanese locale games alike with an easy to select menu.

## Prerequisite Tools
- Locale Emulator(Already packaged in the repo)
- firefox
- lap-clipboard-inserter addon (from https://github.com/laplus-sadness/lap-clipboard-inserter or https://addons.mozilla.org/en-US/firefox/addon/lap-clipboard-inserter/)
- python 3.10 or newer. (This was test on 3.11 but should work for older version)
- Selenium
  ```
  pip install selenium
  ``` 

## Goal
- [x] Add Japanese path support
- [x] Added auto shortcut creation
- [ ] shortcut support japanese named exe
- [ ] Add custom parameter for better usage
- [ ] ~~Seperate the list with folder i.e. make it so that you can put the shortcut into different folder and organize them better.~~
- [x] Add GUI for ease of use

Other Tools are coming soon. ETA Forever.


# New Update
## update 6
Fix relative Paths problem in the firefox's texthooker path when using the Path or pathlib thing.

## update 5
I have added GUI support to the program now. You can now use the GUI instead on the command line. Though it is a bit unstable. But it is usable now. It is in the v4.0 GUI-alpha release. Use the command below in the folder to run it.
```
python mainGUI.py
```

## update 4
I have change to using relative paths instead. Now you don't need to chnage all the file path everytime you move the folder. And you don't even need to be the same path as me anymore.
I have also added the textractor and Locale Emulator directly. You only need to install the locale emulator now. This is almost a one click installer now.

## update 3
I finally manage to open a seperate browser and close it automatically. Now, I only need to find a way to turn on the extension automatically. (Ideas: maybe I could modify the extension itself to work automatically. But I don't know Typescript.)
=======

[![Video tutorial for the tool](https://img.youtube.com/vi/R-oTW-rFl1M?si=v4brWgZpVaLw5T4u/default.jpg)]([https://youtu.be/nTQUwghvy5Q](https://youtu.be/R-oTW-rFl1M?si=v4brWgZpVaLw5T4u))

# NEW GUIDE (V3 and V4 release)

1. Install the locale emulator first. 

2. Clone this repo or download from the release. It is recommended to download from the release as it is more stable.
```
git clone https://github.com/maxkingCS/VN-tools.git
```
3. Extract the .zip file into your VN folder. The VN-tools should now be next to the other VN games. Assuming you got it from the release( Either v4.0 GUI-alpha or v3.0 beta as the time of writing). 
4. Now install selenium.
```
pip install selenium
```

Then get your firefox profile with all extension installed(More info at the NOTE below):
```
%appdata%
AppData\Roaming\Mozilla\Firefox\Profiles # Go to this relative path
```
Then Copy the folder with "default-release" at the end to the VN-tools folder. Rename the profile folder to "profile-default".

* follow 'a' version for V3 and 'b' version for V4.

5a. Run your update list for the first time. This allows the program to store all the VN paths to the executable.(See NOTE below for more info) Use the "update.bat". You should now have VNList.json in the VN-tools folder.

6a. Now you can run the program with the runVN.bat or
```
python VNSelLE.py
```
5b. Now run the mainGUI.py:
```
python mainGUI.py
```
6b. For the first time, you would not see anything in the list. Now click the "Update List" button at the top. It should now refresh with all your VN in a list.

7b. You can click on one of the name and Press "Run Selected" to start the game.

That is it. Just use step 5b whenever you want to run the program.

NOTE: All the VN should be in the VN folder.

The firefox profile must have yomichan and lap-clipboard-inserter extension installed already or install it into the profile later(not test on the second option). yomichan should already be installed with dictionary.
See this for instrction on yomichan: https://learnjapanese.moe/yomichan/

# OLD Guide (V2 and below release)

1. Download the VNSelLE.py and pylnk3.py and put them in the same folder folder. This folder can be anywhere but I put them together with the shortcut for simplicity.
2. You have two options:
- 2a. Make a shortcut of each of your VN and put them in the same folder. (Traditional but Safe and RECOMMENDED)
- 2b. Use the update.bat to automatically make the shortcut. (Experimental and doesn't work for exe with japanese character yet) 
3. Now open the VNSelLE.py and change the value of "folder", "LE" and "tractor" to your own path.
  3.1 folder : where you keep all the shortcut file of the VN.
  3.2 LE     : where you put your Locale Emulator.
  3.3 tractor: where you put your Textractor.(x86)
5. !Recommended! (Optional): Use the NewVNSel.bat if you cannot double click to run the VNSelLE.py or what a quick way to run the script from the desktop. Make sure to change the path to match where you put the VNSelLE.py.  
 Enjoy!
6. If you use a bat file, make sure to change all necessary parameter such as paths and others things to make it work.

## The example paths

~~C:Games/VN(Place your VN in this folder)/VN-tools~~
VN/VN-tools/
local-emulator
the rest of the file.

## Disclaimer
Not all of the file and code are written by me. I merely put together different program into a quick to open way. The texthooker website is from moejapanese way. The clipboard extension is actually called Lap Clipboard Inserter from laplus-sadness.
