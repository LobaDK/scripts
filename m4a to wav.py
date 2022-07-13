import os
import glob
from pathlib import Path
import subprocess

inputfolder = input('Specify folder location: ') #Ask user for folder location
files = glob.glob(os.path.join(inputfolder,'*.m4a')) #Search for and add all m4a's, in the path produced by combining the specified input location, with the m4a file names, and adding them to a list variable named files
if not os.path.isdir(os.path.join(inputfolder,'WAV')): #Check if the folder name WAV, inside the specified folder, exists
    os.makedirs(os.path.join(inputfolder,'WAV')) #Create said WAV folder if not found
for file in files: #Iterate through each file in the files list, saving it to the file variable
    outputfile = Path(file).stem + '.wav' # Remove the file extension from the file and add .wav 
    cmd = ['ffmpeg', '-n', '-i', file, '-b:a', '128k', os.path.join(inputfolder, 'WAV', outputfile)] #Create list variable containing all required arguments. Join specified inputfolder, the WAV folder and the output filename together as the output location for ffmpeg
    subprocess.run(cmd) #Spawn new process and pass the previously created variable with args along with it.
