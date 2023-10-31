import sqlite3
import pandas
from pathlib import Path

def parse_pex_db(path_to_db):
    # Open database
    with sqlite3.connect(path_to_db) as conn:

        # fetch all tables
        cur = conn.cursor()
        tables_sql = cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'; """).fetchall()
        tables = [t[0] for t in tables_sql]

        # Find database version
        db_version_sql = cur.execute("SELECT varvalue as db_version FROM GlobalVars WHERE name='DBVersion'").fetchall()
        db_version = float(db_version_sql[0][0])

        # modification date
        modified_sql = cur.execute("""
            SELECT
            DATETIME(ROUND(LastModification / 1000), 'unixepoch', 'localtime') as modified
            FROM GlobalData""").fetchall()
        modified = modified_sql[0][0]

        if 'OGP' in tables:
            # call correct sql-query
            if 45 <= db_version < 60:
                # Read from db to dataframe
                df = pandas.read_sql_query(Path('organ_programs_dbv45.sql').read_text(), conn)
                # Add None for grid
                df['grid'] = [float('nan')] * len(df)
            elif 60 <= db_version < 72.01:
                df = pandas.read_sql_query(Path('organ_programs_dbv60.sql').read_text(), conn)
            elif 72.01 <= db_version < 74.06:
                df = pandas.read_sql_query(Path('organ_programs_dbv7201.sql').read_text(), conn)
            elif 74.06 <= db_version:
                df = pandas.read_sql_query(Path('organ_programs_dbv7406.sql').read_text(), conn)

        if 'Triplet' in tables:
            if 20.6 <= db_version:
                df = pandas.read_sql_query(Path('c_arm_dbv206.sql').read_text(), conn)

        df['modified'] = modified
    return df
