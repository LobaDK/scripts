import ctypes
import glob
import os
import random
import time
import winreg

set_wallpaper_style = False #default to False
if set_wallpaper_style: #if true, set the wallpaper style to be resized and cropped to fill the screen, while keeping the aspect ratio
    reg_path = r'Control Panel\Desktop\\' #store sub_key location

    WallpaperStyle = 'WallpaperStyle' #store key name
    TileWallpaper = 'TileWallpaper' #store key name

    WallpaperStyle_key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) #open sub_key with write permissions and store in variable
    winreg.SetValueEx(WallpaperStyle_key, WallpaperStyle, 0, winreg.REG_SZ, str(10)) #write new value to WallpaperStyle key to set the new style
    TileWallpaper_key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE) #open sub_key with write permissions and store in variable
    winreg.SetValueEx(TileWallpaper_key, TileWallpaper, 0, winreg.REG_SZ, str(0)) #write new value to TileWallpaper key to disable tiling

rd = r'C:\Users\nichel\Pictures\Elite Dangerous Odyssey'

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