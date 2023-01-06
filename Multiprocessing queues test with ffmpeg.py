from os import path
import time
import signal
import multiprocessing
from queue import Empty
import traceback
import subprocess
from glob import glob
from tqdm import tqdm


class Main():

    def __init__(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        Main.main(self)

    def main(self):
        self.print_lock = multiprocessing.Lock()
        counter = multiprocessing.Value('i', 0)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        # multiprocessing.Event() is like a boolean that can be checked over multiple processes.
        self.shutdown_event = multiprocessing.Event()

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

        threadCount = 12
        processList = []

        p = multiprocessing.Process(target=Main.update_bar, args=(self, bar_queue, fileCount, counter), daemon=True)
        p.start()
        processList.append(p)

        # Create and start all the threads
        for i in range(threadCount):
            p = multiprocessing.Process(target=Main.ffmpegThread, args=(self, inQueue, bar_queue, counter), daemon=True)
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


    def signal_handler(sig, frame, self):
        self.print_lock.acquire()
        print(f"Waiting for last file on {multiprocessing.current_process().name}.")
        self.print_lock.release()
        self.shutdown_event.set()
    
    def update_bar(self, q, fileCount, counter):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        pbar = tqdm(total=fileCount, unit='files')

        while not self.shutdown_event.is_set() and not counter.value == fileCount:
            try:
                x = q.get(timeout=1)
                pbar.update(x)
            except Empty:
                pass

    def ffmpegThread(self, inQueue, bar_queue, counter):
        signal.signal(signal.SIGINT, lambda signum, frame: Main.signal_handler(signum, frame, self))
        #signal.signal(signal.SIGINT, signal_handler)

        # There's a try around everything so if something breaks it doesn't stop all the other threads.
        try:
        
            # Wait for files to start showing in the queue, then wait a bit longer.
            while inQueue.empty():
                time.sleep(1)
            
            # Convert files until ctrl+c or the queue's empty.
            while not self.shutdown_event.is_set():
                try:
                    file = inQueue.get(timeout=1)
                    
                    if path.isfile(file[1][3]):
                        subprocess.run(file[1], stderr=subprocess.PIPE, creationflags=subprocess.DETACHED_PROCESS)
                        with counter.get_lock():
                            counter.value += 1
                        
                        if not self.shutdown_event.is_set():
                            bar_queue.put(1, block=False)
                        
                except Empty:
                    break
                    
            # This is outside the try/catch as queues block a thread from stopping till they're closed, so always need to be run.
            inQueue.close()
            self.print_lock.acquire()
            print(f"Shutting down {multiprocessing.current_process().name}")
            self.print_lock.release()
        except Exception as e:
            traceback.print_exc()


if __name__ == '__main__':
    Main()
    

