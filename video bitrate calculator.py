file_size = float(input('\nInput the desired filesize in megabytes: ')) #convert user input for file size to float
video_lenght = float(input('\nInput the videos lenght in seconds: ')) #convert user input for video lenght to float
audio_bitrate = float(input('\nInput the audio bitrate in kilobytes: ')) #convert user input for audio bitrate to float
bitrate = (file_size * 8192) / video_lenght - audio_bitrate #multiply file size with 8192, turning it into kilobytes. Then divide it with the video lenght, and subtract the audio bitrate, giving the total required kilobytes a second, for the video portion

print('\n%.2f kilobytes a second for the video' % bitrate) #print calculated video bitrate and the first 2 decimal points
input('\nPress any key to continue...') #prevent script from exiting until the user is done