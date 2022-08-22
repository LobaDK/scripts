import os

for path, currentDirectory, files in os.walk("CHANGEME"):
    for file in files:
        extension = os.path.splitext(file)
        if extension[1] == extension[1].upper():
            file_without_ext, ext = os.path.splitext(file)
            ext = ext.lower()
            newfile = file_without_ext + ext
            print(f'renaming {os.path.join(path, file)} to {os.path.join(path,newfile)}')
            try:
                os.rename(os.path.join(path, file), os.path.join(path, newfile))
            except:
                print("Error renaming file. Original filename and path has been logged to 'failedrename.log")
                try:
                    with open('failedrename.log', 'a') as f:
                        f.write(os.path.join(path, file))
                except:
                    print('Writting to log failed')