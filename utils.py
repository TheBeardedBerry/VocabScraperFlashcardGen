import datetime
from os import path, mkdir, rename

def backup_file(file_path):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    directory, file = path.split(file_path)

    extension = file.split('.')[-1]
    basename = file.split('.')[0]

    new_name = f"{basename}.{timestamp}.{extension}"
    new_directory = path.join(directory, 'backup')
    if not path.exists(new_directory):
        mkdir(new_directory)

    new_location = path.join(new_directory, new_name)
    rename(file_path, new_location)