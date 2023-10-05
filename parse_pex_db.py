import sqlite3
import pandas


def parse_pex_db(path_to_db):
    # Open database
    conn = sqlite3.connect(path_to_db)

    # Find database version
    sql_db_version = """SELECT * FROM GlobalVars
                        WHERE GlobalVars.Name = 'DBVersion'"""
    global_vars = pandas.read_sql_query(sql_db_version, conn)
    db_version = float(global_vars.iloc[:, 1][0])

    # call correct sql-query
    if 45 <= db_version < 60:
        fd = open('organ_programs_dbv45.sql', 'r')
        sql_organ_programs = fd.read()
        fd.close()
        # Read from db to dataframe
        df = pandas.read_sql_query(sql_organ_programs, conn)
        # Add None for grid
        df['grid'] = [float('nan')] * len(df)
    elif 60 <= db_version < 72.01:
        fd = open('organ_programs_dbv60.sql', 'r')
        sql_organ_programs = fd.read()
        fd.close()
        # Read from db to dataframe
        df = pandas.read_sql_query(sql_organ_programs, conn)
    elif 72.01 <= db_version < 74.06:
        fd = open('organ_programs_dbv7201.sql', 'r')
        sql_organ_programs = fd.read()
        fd.close()
        # Read from db to dataframe
        df = pandas.read_sql_query(sql_organ_programs, conn)
    elif 74.06 <= db_version:
        fd = open('organ_programs_dbv7406.sql', 'r')
        sql_organ_programs = fd.read()
        fd.close()
        # Read from db to dataframe
        df = pandas.read_sql_query(sql_organ_programs, conn)

    # close database
    conn.close()

    return df
