from os import walk, path, listdir, mkdir, stat, remove
from subprocess import CalledProcessError, run
import logging

# Set logger settings
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename='converter.log', filemode='a', level=logging.DEBUG)

output_folder = 'AV1'

# Iterate through my clips folder structure
# Recordings
#     └Name of the game
#           └Edited
#               └lossless
#               └AV1
try:
    logging.info('#################'
                 '\n\t\t\t#Starting script#'
                 '\n\t\t\t#################')
    for root, dirs, files in walk(r'E:\Recordings'):
        for dirname in dirs:
            # If the folder is the "lossless" folder where I keep my edited clips
            if dirname == 'lossless':
                
                # Log "lossless" folder location
                logging.info(f'Found {path.join(root, dirname)}!')

                # Get list of files and iterate over them.
                # If folder is empty, an empty list will be returned, and thus not run
                for filename in listdir(path.join(root, dirname)):

                    # I exlusively work with the mp4 and mkv containers.
                    # If the file does not have either, assume it should be ignored
                    if path.splitext(filename)[1].casefold() == ('.mkv' or '.mp4'):
                        logging.info(f'Skipping {filename_converted}. Reason: Not an mp4 or mkv container')
                        continue

                    # Use the root folder variable to create a variable
                    # containing the path for the converted folder
                    # and a variable containing the path as well as filename
                    # for the new converted file
                    dirname_converted = path.join(root, output_folder)
                    filename_converted = path.join(root, output_folder, f"{path.splitext(filename)[0]}.mp4")

                    # Check if the folder for converted clips does not exist
                    # and create it, as well as log it, if it does not
                    # If it fails, it will instead log the exception and continue with the next file/folder
                    if not path.exists(dirname_converted):
                        try:
                            mkdir(dirname_converted)
                            logging.info(f'Created {dirname_converted}.')
                        except OSError as e:
                            logging.exception('Exception occurred')
                            continue

                    # Check if a file with the same name already exists
                    # in the converted folder.
                    # If it is 1,048,576 bytes (1 megabyte) or less
                    # delete, log and convert it.
                    # Otherwise, assume it has aleady been converted and log it
                    if path.exists(filename_converted):
                        if stat(filename_converted).st_size <= 1_048_576:
                            remove(filename_converted)
                            logging.info(f'Removed {filename_converted} due to being 1 megabyte or less in size')
                        
                        else:
                            logging.info(f'Skipping {filename_converted}. Reason: Already exists')
                            continue
                    
                    # Let the user know which file is about to be converted, and log it
                    print(f'\nConverting {path.join(root, dirname, filename)}\n')
                    logging.info(f'Converting {path.join(root, dirname, filename)}.')
                    
                    # Create a list with ffmpeg and it's paramters, for a high-quality medium-slow AV1 encoding
                    # a CRF of 45 may seem too high, but it's the perfect mix between
                    # low filesize and good-enough quality for online sharing.
                    cmd = ['ffmpeg', '-n', '-i', f'{path.join(root, dirname, filename)}', '-c:v',
                        'libsvtav1', '-preset', '4', '-crf', '45', '-b:v', '0', '-c:a', 'aac', '-b:a',
                        '192k', '-movflags', '+faststart',
                        filename_converted]

                    # Attempt to run command, and assume any non-zero codes are bad
                    # This isn't the best, but in our case it should be more than fine
                    # If exit-code is non-zero, log the exception and continue with the next file
                    try:
                        run(cmd, check=True)
                    except CalledProcessError as e:
                        logging.exception('Exception occurred')

            # Log folders ignored by the script
            else:
                logging.info(f'Ignoring folder {path.join(root, dirname)}.')

    logging.info('#####################################'
                 '\n\t\t\t#Nothing to do. Shutting down script#'
                 '\n\t\t\t#####################################')

except KeyboardInterrupt:
    logging.info('##########################################'
                 '\n\t\t\t#Interrupt received. Shutting down script#'
                 '\n\t\t\t##########################################')