from parse_pex_db import parse_pex_db
import os
import sys
from zipfile import ZipFile

# input_directory from command line
input_directory = sys.argv[1]
print(f'input_directory: {input_directory}')

# find all .zip in input_directory
for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.lower().endswith(".zip"):
            # open zip
            with ZipFile(os.path.join(root, file), 'r') as z:
                # list of zips with .sqlite file
                file_name = [s for s in z.namelist() if '.sqlite' in s]
                z.extract(file_name[0], root)

# find all .sqlite in input_directory
for root, dirs, files in os.walk(input_directory):
    for file in files:
        if file.lower().endswith(".sqlite"):
                print(file)
                # parse temporary sqlite database
                df = parse_pex_db(os.path.join(root, file))

                # save dataframe as csv
                [pre, ext] = os.path.splitext(file)
                csv_path = os.path.join(root, pre + ".csv")
                df.to_csv(csv_path)

