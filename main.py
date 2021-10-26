from parse_pex_db import parse_pex_db
import os


# for all mdb files in folder databases
for root, dirs, files in os.walk('databases'):
    for file in files:
        if file.endswith(".sqlite"):
            print(file)

            # parse temporary sqlite database
            df = parse_pex_db(os.path.join(root, file))

            # save dataframe as csv
            [pre, ext] = os.path.splitext(file)
            csv_path = os.path.join(root, pre + ".csv")
            df.to_csv(csv_path)