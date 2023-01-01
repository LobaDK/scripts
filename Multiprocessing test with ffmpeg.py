from multiprocessing import Pool
import subprocess
from glob import glob
from os import path
from tqdm import tqdm

def convert(file: str):
    arg = ['ffmpeg', '-i', file, '-b:a', '192k', path.join(r'C:\Users\nickl\Music\test', path.basename(file) + '.mp3')]
    subprocess.run(arg, stderr=subprocess.DEVNULL)
    print(f'Converted {path.basename(file)}')

def main():
    files = glob(r'C:\Users\nickl\Music\FavoriteMusic\*.m4a')

    with Pool() as pool:
        pool.map(convert, files)

if __name__ == '__main__':
    main()
