from parse_pex_db import parse_pex_db
from mdb2sqlite import mdb2sqlite
import os


# for all mdb files in folder mdb_databases
for root, dirs, files in os.walk('mdb_databases'):
    for file in files:
        if file.endswith(".mdb"):
            print(file)

            # convert database from mdb to sqlite
            mdb_database_path = os.path.join(root, file)
            mdb2sqlite(mdb_database_path)

            # parse temporary sqlite database
            [machine, df] = parse_pex_db()

            # save dataframe as csv
            [pre, ext] = os.path.splitext(file)
            csv_path = os.path.join(root, pre + ".csv")
            df.to_csv(csv_path)