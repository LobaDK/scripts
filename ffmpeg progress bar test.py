import subprocess
from json import loads
from tqdm import tqdm
from pathlib import Path

file = r"C:\Users\nichel\Downloads\Recordings\Grand Theft Auto V\GTA5 Scramjet vs nerfed Oppressor mk2 2023-02-05 23-21-28.mp4"

cmd = [r"C:\Users\nichel\Downloads\Recordings\Grand Theft Auto V\ffmpeg.exe",
       '-y',
       '-i',
       file,
       '-v',
       'quiet',
       '-progress',
       '-',
       '-c:v',
       'h264',
       '-c:a',
       'copy',
       r"C:\Users\nichel\Downloads\Recordings\Grand Theft Auto V\GTA5 Scramjet vs nerfed Oppressor mk2 2023-02-05 23-21-28.mkv"]

cmd2 = [r"C:\Users\nichel\Downloads\Recordings\Grand Theft Auto V\ffprobe.exe", '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=nb_frames', '-of', 'json', file]

pp = subprocess.run(cmd2, capture_output=True)

frames = int(loads(pp.stdout)['streams'][0]['nb_frames'])

progress_bar = tqdm(total=frames, unit='frames', desc=f'Converting {Path(file).stem}')

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while True:
       stdout = p.stdout.readline().decode()
       stdout = stdout.replace('\n', '')
       if 'frame=' in stdout:
              progress_bar.update(int(stdout.split('=')[1]) - progress_bar.n)
       if 'progress=' in stdout:
              if stdout.split('=')[1] == 'end': break

progress_bar.close()
