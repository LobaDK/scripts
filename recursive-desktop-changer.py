import ctypes
import glob
import os
import random
import time

rd = r'CHANGE_ME_TO_IMAGE_FOLDER_LOCATION'

files = glob.glob('**/*.png',recursive=True, root_dir=rd)

while True:
    random_image = os.path.join(rd, random.choice(files))
    print(f'Changing to {random_image}...')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, random_image, 0)
    time.sleep(300)