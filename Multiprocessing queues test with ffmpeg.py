from os import path
import time
import signal
import multiprocessing
from queue import Empty
import traceback
import subprocess
from glob import glob
from tqdm import tqdm

# multiprocessing.Event() is like a boolean that can be checked over multiple processes.
#shutdown_event = multiprocessing.Event()
def signal_handler(sig, frame):
    print("Waiting for last files.")
    global shutdown_event
    shutdown_event.set()

def update_bar(shutdown_event, q, fileCount):
    pbar = tqdm(total=fileCount, unit='files')

    while not shutdown_event.is_set():
        try:
            x = q.get()
            pbar.update(x)
        except KeyboardInterrupt:
            pass

def ffmpegThread(shutdown_event, inQueue, bar_queue):
    #signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # There's a try around everything so if something breaks it doesn't stop all the other threads.
    try:
    
        # Wait for files to start showing in the queue, then wait a bit longer.
        while inQueue.empty():
            time.sleep(1)
        
        # Convert files until ctrl+c or the queue's empty.
        while not shutdown_event.is_set():
            try:
                file = inQueue.get(timeout=10)
                
                if path.isfile(file[1][3]):
                    si = subprocess.STARTUPINFO()
                    si.dwFlags = subprocess.CREATE_BREAKAWAY_FROM_JOB | subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
                    time.sleep(1)
                    #p = subprocess.Popen(file[1], stderr=subprocess.PIPE, creationflags=subprocess.DETACHED_PROCESS)
                    #time.sleep(1)
                    #p.communicate()
                    # FFmpeg steals the 'CTRL + C', or SIGINT, signal even when signal.signal is used
                    # So a mix of checking the returncode and output of ffmpeg is used instead
                    # if p.returncode == 0:
                    #     pass
                    # elif p.returncode != 0 and 'already exists' in p.stderr.decode():
                    #     pass
                    # elif p.returncode != 0 and  'Exiting normally' in p.stderr.decode():
                    #     shutdown_event.set()
                    # elif p.returncode == 3221225786 and p.stderr.decode() == '':
                    #     shutdown_event.set()
                    # else:
                    #     print('Error detected in ffmpeg, stopping...')
                    #     shutdown_event.set()
                    
                    if not shutdown_event.is_set():
                        bar_queue.put(1, block=False)
                    
            except Empty:
                print("inQueue Empty")
                break
                
        # This is outside the try/catch as queues block a thread from stopping till they're closed, so always need to be run.
        inQueue.close()
        print("Thread shutdown")
    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    shutdown_event = multiprocessing.Event()
    # Queues are the multiprocessing version of lists.
    inQueue = multiprocessing.Queue()
    bar_queue = multiprocessing.Queue()
    
    # Set up the queue with the current file number and command, so we can track progress.
    files = glob(r'C:\Users\nichel\Music\FavoriteMusic\*.m4a')
    fileCount = 0
    for file in files:
        fileCount += 1
        command = ['ffmpeg', '-n', '-i', file, '-b:a', '192k', path.join(r'C:\Users\nichel\Music\test', path.basename(file) + '.mp3')]
        inQueue.put([fileCount, command])
    
    threadCount = 1
    processList = []

    p = multiprocessing.Process(target=update_bar, args=(shutdown_event, bar_queue, fileCount), daemon=True)
    p.start()
    processList.append(p)

    # Create and start all the threads
    for i in range(threadCount):
        p = multiprocessing.Process(target=ffmpegThread, args=(shutdown_event, inQueue, bar_queue), daemon=True)
        p.start()
        processList.append(p)
    
    # Join them one at a time, so it'll only continue when they're all closed.
    for p in processList:
        p.join()

    # Empty any left-over items from the queue until it is empty 
    # to avoid QueueFeederThread from deadlocking the script
    # or becoming a zombie processes that prevents returning to the terminal
    try:
        while True:
            _ = inQueue.get(block=False)
    except Empty:
        pass

    print("Exited.")


