import os

def print_directory_structure(rootdir):
    for foldername, subfolders, filenames in os.walk(rootdir):
        print(f'[{foldername}]')
        for subfolder in subfolders:
            print(f'  - {subfolder}')
        for filename in filenames:
            print(f'  - {filename}')

# Get the current working directory
current_directory = os.getcwd()

# Print the directory structure for the current directory
print_directory_structure(current_directory)
