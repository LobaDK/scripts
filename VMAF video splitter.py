import json
import math
import subprocess
import glob

scene_cuts = 5
start_frame = 0
filename = "test.mp4"

arg1 = ['ffprobe', '-v', 'quiet', '-show_streams', '-select_streams', 'v:0', '-of', 'json', filename]

stream = subprocess.Popen(arg1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

stdout, stderr = stream.communicate()

video_metadata = json.loads(stdout)['streams'][0]

total_frames = int(video_metadata['nb_frames'])

for i in range(scene_cuts):
    end_frame = math.floor((total_frames / scene_cuts) * (i + 1))
    arg2 = ['ffmpeg', '-n', '-ss', str(start_frame / 60), '-to', str(end_frame / 60), '-i', filename, '-c:a', 'aac', '-c:v', 'libsvtav1', '-crf', '43', '-b:v', '0', '-b:a', '192k', '-g', '600', '-preset', '10', '-movflags', '+faststart', f'scene_split{i}.mp4']
    print(f'Cutting from frame {start_frame} to frame {end_frame}')
    subprocess.run(arg2)
    start_frame = end_frame + 1

""" ii = 0
for file in glob.glob('scene_split*.mp4'):
    ii += 1
    end_frame = math.floor((total_frames / scene_cuts) * (ii + 1))
    arg3 = ['ffmpeg', '-n', '-i', file, '-c:a', 'aac', '-c:v', 'libsvtav1', '-crf', '43', '-b:v', '0', '-b:a', '192k', '-g', '600', '-preset', '8', '-movflags', '+faststart', f'converted_scene{ii}.mp4']
    print(f'Cutting from frame {start_frame} to frame {end_frame}')
    subprocess.run(arg3)
    start_frame = end_frame + 1 """

concat_file = open('concatlist.txt', 'a')
files = glob.glob('scene*.mp4')
for file in files:
    concat_file.write(f"file '{file}'\n")

concat_file.close()

arg3 = ['ffmpeg', '-safe', '0', '-f', 'concat', '-i', 'concatlist.txt', '-c:v', 'copy', '-c:a', 'copy', 'output.mp4']
subprocess.run(arg3)