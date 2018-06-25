import pyodbc
import sqlite3
from collections import namedtuple
import re


def mdb2sqlite(mdb_database_path):

    # Open Access Database
    # Need to install driver for Access - Access Database Engine
    conn_str = (
        r'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};'
        r'DBQ={};'
        ).format(mdb_database_path)
    cnxn = pyodbc.connect(conn_str)

    # Need to change encoding to read the Access database - latin1 seams to work
    cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin1')
    cursor = cnxn.cursor()

    conn = sqlite3.connect('temp.db')
    c = conn.cursor()

    Table = namedtuple('Table', ['cat', 'schem', 'name', 'type'])

    # get a list of tables
    tables = []
    for row in cursor.tables():
        if row.table_type == 'TABLE':
            t = Table(row.table_cat, row.table_schem, row.table_name, row.table_type)
            tables.append(t)

    for t in tables:
        # print(t.name)

        # SQLite tables must being with a character or _
        t_name = t.name
        if not re.match('[a-zA-Z]', t.name):
            t_name = '_' + t_name

        # SQLite table names cannot contain space
        t_name = t_name.replace(" ", "_")

        # get table definition
        columns = []
        for row in cursor.columns(table=t.name):
            # print('    {} [{}({})]'.format(row.column_name, row.type_name, row.column_size))
            col_name = re.sub('[^a-zA-Z0-9]', '_', row.column_name)
            if col_name.upper() == 'DEFAULT':
                col_name = '{}{}'.format(col_name, t_name)
            # SQLite cannot have columns named INDEX
            if col_name.upper() == 'INDEX':
                col_name = 'Id'
            # Data type BIT -> TEXT
            if row.type_name == 'BIT':
                row.type_name = 'TEXT'

            # No need to specify size for column type
            # columns.append('{} {}({})'.format(col_name.capitalize(), row.type_name, row.column_size))
            columns.append('{} {}'.format(col_name.capitalize(), row.type_name))
        cols = ', '.join(columns)

        # create the table in SQLite
        c.execute('DROP TABLE IF EXISTS "{}"'.format(t_name))
        c.execute('CREATE TABLE "{}" ({})'.format(t_name, cols))

        # copy the data from MDB to SQLite
        cursor.execute('SELECT * FROM "{}"'.format(t.name))
        for row in cursor:
            values = []
            for value in row:
                if value is None:
                    values.append(u'NULL')
                else:
                    if isinstance(value, bytearray):
                        value = sqlite3.Binary(value)
                    else:
                        value = u'{}'.format(value)
                    values.append(value)
            v = ', '.join(['?'] * len(values))
            sql = 'INSERT INTO "{}" VALUES(' + v + ')'
            c.execute(sql.format(t_name), values)

    conn.commit()
    conn.close()
