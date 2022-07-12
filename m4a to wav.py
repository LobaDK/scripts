import os
import glob
from pathlib import Path
import subprocess

inputfolder = input('Specify folder location: ')
files = glob.glob(os.path.join(inputfolder,'*.m4a'))
if not os.path.isdir(os.path.join(inputfolder,'WAV')):
    os.makedirs(os.path.join(inputfolder,'WAV'))
for file in files:
    outputfile = Path(file).stem + '.wav'
    cmd = ['ffmpeg', '-n', '-i', file, '-b:a', '128k', os.path.join(inputfolder, 'WAV', outputfile)]
    subprocess.run(cmd)