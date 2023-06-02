import subprocess
from json import loads
from tqdm import tqdm
from pathlib import Path

file = r"C:\Users\nichel\Downloads\Recordings\Grand Theft Auto V\GTA5 Scramjet vs nerfed Oppressor mk2 2023-02-05 23-21-28.mp4"

# command for converting the file.
# We use "-v fatal" to hide everything except fatal exits.
# "-progress" to instead display a bunch 
# of lines with data that constantly updates
# and the "-" right after to pipe it to stdout
cmd = [r"C:\Users\nichel\Downloads\Recordings\Grand Theft Auto V\ffmpeg.exe",
       '-n',
       '-i',
       file,
       '-v',
       'fatal',
       '-progress',
       '-',
       '-c:v',
       'h264',
       '-c:a',
       'copy',
       r"C:\Users\nichel\Downloads\Recordings\Grand Theft Auto V\GTA5 Scramjet vs nerfed Oppressor mk2 2023-02-05 23-21-28.mkv"]

# Command for getting the total frames from the input file
# "-of json" insures we get it in a nice readable format
# for the json module to easily parse
cmd2 = [r"C:\Users\nichel\Downloads\Recordings\Grand Theft Auto V\ffprobe.exe", '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=nb_frames', '-of', 'json', file]

# Get the total frames first
pp = subprocess.run(cmd2, capture_output=True)

# Save the returned total frames
frames = int(loads(pp.stdout)['streams'][0]['nb_frames'])

# Create the progress bar
progress_bar = tqdm(total=frames, unit='frames', desc=f'Converting {Path(file).stem}')

# Start ffmpeg process in the background and pipe the outputs.
# Reading from stderr if there is nothing will lock up the script
# so we're instead piping stderr to stdout as we know something
# will always be written to it, and then handling the logic from there
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, )

# Run an infinite loop
while True:
       # Decode the output to pure text
       stdout = p.stdout.readline().decode()
       
       # Get rid of newlines. It's not actually required
       # but it bothers me knowing each 2nd line is basically empty
       # without it
       stdout = stdout.replace('\n', '')
       
       # if the current string in our output is the frames progress
       if 'frame=' in stdout:

              # Add only the new frames by subtracting the total converted with the total progress
              progress_bar.update(int(stdout.split('=')[1]) - progress_bar.n)
       
       # If the current string in our output instead is the returned progress type.
       # ffmpeg uses this to display if it's done or not, by being either "continue"
       # or "end"
       if 'progress=' in stdout:

              # if the progress is end, it means it's done converting, and we can break out of the loop
              if stdout.split('=')[1] == 'end': break

       # If the process exited due to the file already existing
       if 'already exists' in stdout:
              break

progress_bar.close()
