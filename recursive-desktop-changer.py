import ctypes
import glob
import os
import random
import time

rd = r'CHANGE_ME_TO_IMAGE_FOLDER_LOCATION'

files = glob.glob('**/*.png',recursive=True, root_dir=rd) #use glob to recursively get all file locations from specified folder

SPI_SETDESKWALLPAPER = 20 #converted hex code 0x0014 to decimal

random.shuffle(files) #shuffle the list on first run each time, for a little extra randomness

while True: #enter infinite loop
    random_image = os.path.join(rd, random.choice(files)) #join the root path with a randomly picked file from glob
    print(f'Changing to {random_image}...\n')
    wallpaper_changed = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, random_image, 0) #use SystemParametersInfoW to change desktop wallpaper and save exit code to variable
    if not bool(wallpaper_changed): #if false, print in the terminal that an error occured
        print('Error applying wallpaper!\n')
    time.sleep(300) #wait 5 minutes before applying a new wallpaper