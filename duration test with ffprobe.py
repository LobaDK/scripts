from glob import glob
from json import loads
from subprocess import run

length: float = 0
for file in glob('*.mp4'):
    p = run(['ffprobe', '-v', 'quiet', '-show_streams', '-select_streams', 'v', '-of', 'json', file], capture_output=True)
    data = loads(p.stdout)['streams'][0]
    duration = str(data['duration'])
    print(duration)
print(length)
