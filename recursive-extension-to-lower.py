import os

for path, currentDirectory, files in os.walk("D:\OBS"):
    for file in files:
        extension = os.path.splitext(file)[1]
        if not extension:
            continue
        if extension == extension.upper():
            file_without_ext, ext = os.path.splitext(file)
            if not file_without_ext:
                continue
            ext = ext.lower()
            newfile = file_without_ext + ext
            print(f'renaming {os.path.join(path, file)} to {os.path.join(path,newfile)}')
            try:
                os.rename(os.path.join(path, file), os.path.join(path, newfile))
            except:
                print("Error renaming file. Original filename and path has been logged to 'failedrename.log")
                try:
                    with open('failedrename.log', 'a') as f:
                        f.write(f'{os.path.join(path, file)}\n')
                except:
                    print('Writting to log failed')
