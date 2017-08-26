import sqlite3
import os
from collections import OrderedDict as odict
from pprint import pprint

from src import browser_setup







def _connect_db(db_file):
    """
    Establishes connection to the database file, returns connection, cursor objects and filename.
    :param db_file: Path of the database file.
    :type db_file: str/path-like object
    :return: conn, cur filename
    :rtype: connection object, cursor object, str
    """
    if not os.path.exists(db_file):
        print("ERROR: Invalid path. ({})".format(db_file))
        print("Quitting...")
        quit()
    conn = sqlite3.connect(database=db_file)
    cur = conn.cursor()
    return conn, cur, os.path.split(db_file)[1]


def _db_tables(cursor):
    """
    Returns names of tables from the cursor object of the database file.
    :param cursor: Cursor object attached to the database file, from _connect_db function.
    :type cursor: Connection.Cursor Object
    :return: list of table names in database file.
    :rtype: list['str']
    """
    query = "SELECT name FROM sqlite_master WHERE type = 'table'"
    return [table_[0] for table_ in cursor.execute(query)]


def _table_records(cursor, table):
    """
    Yields one record (row) of the table, whenever called.

    Usage:
        table_records_generator = _table_records(cursor, table)
        next_record_in_table = next(table_records_generator)
    :param cursor: Cursor object for current database file
    :type cursor: Connection.Cursor object
    :param table: Name of table
    :type table: str
    :return: Yields tuple of record, each column separated by a comma
    :rtype: tuple[str, *str, ...]
    """
    query = '''SELECT * FROM {}'''.format(table)
    cursor.execute(query)
    field_names = [desc_[0] for desc_ in cursor.description]
    yield field_names
    for record_ in cursor:
        yield record_


def _make_records_dict_generator(records: 'iterable', table=None, filepath=None):
    record_dict = [odict({'_filepath': filepath, 'table': table})]
    # pprint(list(records))
    # quit()
    field_names = next(records)
    for record_ in records:
        yield {field_name_: field_
                     for field_name_, field_ in zip(field_names, record_)}
    # return record_dict


def firefox():
    profile_paths = browser_setup.setup_profile_paths()
    file_paths = browser_setup.db_filepath(root=profile_paths, filenames='places', ext='sqlite')
    for idx, file_ in enumerate(file_paths):
        print('\n', '=' * 50, '\n')
        # conn, cur, filename = _connect_db(db_file=file_)
        # tables = _db_tables(cursor=cur)
        tables = ['moz_places']
        for table_ in tables:
            print('.' * 8)
            conn, cur, filename = _connect_db(db_file=file_)
            records = _table_records(cursor=cur, table=table_)
            prepped_records_generator = _make_records_dict_generator(records=records, table=table_, filepath=file_)
            prepped_records = list(prepped_records_generator)
            pprint(prepped_records)
            cur.close()


def chrome():
    file_paths = browser_setup.db_filepath(
        root="C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default",
        filenames='History', ext=None)
    for idx, file_ in enumerate(file_paths):
        print('\n', '=' * 50, '\n')
        conn, cur, filename = _connect_db(db_file=file_)
        tables = _db_tables(cursor=cur)
        for table_ in tables:
            print('.' * 8)
            conn, cur, filename = _connect_db(db_file=file_)
            records = _table_records(cursor=cur, table=table_)
            prepped_records = _make_records_dict_generator(records=records, table=table_, filepath=file_)
            pprint(prepped_records)
            cur.close()
    
    "C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"


if __name__ == '__main__':
    firefox()
    # chrome()
