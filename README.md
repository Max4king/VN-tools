# VN-tools

This is where I plan to make my own tools to make playing vn easier.

## What can this do?
This program helps you run the VN quicker. It runs the Locale Emulator and Textractor within one step. It can also help you organize your VN and japanese locale games alike with an easy to select menu.

## Prerequisite Tools
- Locale Emulator
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
- [ ] Seperate the list with folder i.e. make it so that you can put the shortcut into different folder and organize them better.
- [ ] Add GUI for ease of use

Other Tools are coming soon. ETA Forever.

# New Update
## update 3
I finally manage to open a seperate browser and close it automatically. Now, I only need to find a way to turn on the extension automatically. (Ideas: maybe I could modify the extension itself to work automatically. But I don't know Typescript.)

## update 2
I have added a way to easily add new shortcut without manually making shortcut for every game that doesn't have japanese exe name.
## update 1
I have just made a python version of the program so that it is easier to read and manage in the future.


# Guide

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
C:Games/VN(Place your VN in this folder)/VN-tools


## vnSelectorLE (Deprecated and Legacy version)
This is used along with Locale Emulator. This BAT script is use to make launching VN a little easier by having a list of vn along with using the Locale Emulator for you without right clicking it everytime.
NOTE: To make this work. You need to make a shortcut to the VN .exe file into one folder. Then you either place the vnSelectorLE inside it or change the directory that the BAT file points to.

## Disclaimer
Not all of the file and code are written by me. I merely put together different program into a quick to open way. The texthooker website is from moejapanese way. The clipboard extension is actually called Lap Clipboard Inserter from laplus-sadness.
