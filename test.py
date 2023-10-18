from selenium import webdriver
from time import sleep
options = webdriver.FirefoxOptions()
options.add_argument("--profile")
options.add_argument("C:\Games\VN\VN-tools\profile-default")
driver = webdriver.Firefox(options=options)
folder = "C:/Games/VN/VN-tools"
html_file_path = folder + "/TexthookerOffline/TextHooker.htm"
driver.get(html_file_path)
sleep(5)
driver.quit()
