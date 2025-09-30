### Jan 22 2024 test 2
import os
from datetime import datetime

# Specify the subdirectory name
subdirectory = "experiment_data"
appendcount = 0

def write_data(data):
    # Append to the text file
    with open(csv_filepath, 'a', newline='', encoding='utf-8') as textfile:
        # print("Clicked in empty location:",event.pos[0], event.pos[1], file=f) 
        print(data, file=textfile)

    # print(f"Data appended to text file: {csv_filepath}")

# Create the subdirectory if it doesn't exist
if not os.path.exists(subdirectory):
    os.makedirs(subdirectory)

print(os.listdir(subdirectory))
files = {}
filemax = 0
for index, file in enumerate(os.listdir(subdirectory)):
    filenumber = 0  # Initialize filenumber here
    # print('one file here', file)
    try:
        filenumber = int(file.split('_')[0])  # Extract the part before the first '_'
        # print('file number', filenumber)

        if filenumber > filemax:
            filemax = filenumber
            # print('Filemax', filemax)
    except ValueError:
        # Handle the exception if conversion to int fails
        pass

    # print(index, filenumber, filemax)

# File paths
today_date = datetime.today().strftime('%Y-%m-%d')
csv_filename = f"{filemax + 1}_{today_date}.txt"
csv_filepath = os.path.join(subdirectory, csv_filename)