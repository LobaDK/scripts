import os

for path, currentDirectory, files in os.walk("CHANGEME"): #recursively walk specified directory, saving path to each file to "path" variable, saving the folder names to "currentDirectory", and saving the filenames to "files"
    for file in files: #loop through each file in files variable
        extension = os.path.splitext(file)[1] #grab the second value in the returned tuple, which is the extension
        if not extension: #if the file has no extension, skip
            continue
        if extension == extension.upper(): #check if extension is in uppercase
            file_without_ext, ext = os.path.splitext(file) #split filename and extension, and save tuple into it's respective variables
            if not file_without_ext: #skip if the file is only an extension (.bashrc, .env, .hidden) for example
                continue
            ext = ext.lower() #convert extension to lowercase
            newfile = file_without_ext + ext #combine filename and new lowercased extension
            print(f'renaming {os.path.join(path, file)} to {os.path.join(path,newfile)}') #print old to new filename for convinience
            try:
                os.rename(os.path.join(path, file), os.path.join(path, newfile)) #combine path and new filename, and attempt to rename it to the lowercased extension version
            except:
                print("Error renaming file. Original filename and path has been logged to 'failedrename.log") #print if the renaming failed
                try:
                    with open('failedrename.log', 'a') as f: #attempt to open file
                        f.write(f'{os.path.join(path, file)}\n') #attempt to write the original filename to log
                except:
                    print('Writting to log failed') #print if writting to log also failed
