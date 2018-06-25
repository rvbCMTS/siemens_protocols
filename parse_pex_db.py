import sqlite3
import pandas


def parse_pex_db():
    # Open temporary database
    conn = sqlite3.connect('temp.db')

    # Open and read the sql query
    fd = open('machine.sql', 'r')
    sql_machine = fd.read()
    fd.close()
    fd = open('organ_programs.sql', 'r')
    sql_organ_programs = fd.read()
    fd.close()

    # Read from db to dataframe
    machine = pandas.read_sql_query(sql_machine, conn)
    df = pandas.read_sql_query(sql_organ_programs, conn)

    # Correcting kV och mAs
    df.kv = df.kv/10
    df.mas = df.mas/100

    # close database
    conn.close()

    return machine, df
