import sqlite3
import os
from pprint import pprint


def setup_paths():
    """
    Sets up the directory path for sqlite database files"
    :return: root directory
    :rtype: str/path-like object
    """
    return os.path.realpath(os.path.join(os.path.split(__file__)[0],
                                         'data', 'firefox_regular_surfing')
                            )


def filepath(root, filenames= ['places', 'storage'], ext='sqlite'):
    """
    Yields the path for the next database file.
    By default, these are sqlite file. (used by browsers to store history, bookmarks etc)
    
    Usage:
        filepath_generator = filepath(root, filenames, ext)
        next_sqlite_databse_filepath = next(filepath_generator)
        
    :param root: Directory path containing the database files.
        Default: <project_root>/tinker/data/firefox_regular_surfing/
    :type root: str/path-like object
    :param filenames: List of database filenames in the root directory.
        Default: ['places', 'storage']
    :type filenames: list[str]
    :param ext: Extension of the databse file.
        Default: sqlite
    :type ext: str
        Default: sqlite
    :return: yields path of the database file.
    :rtype: str/path-like object
    """
    for file_ in filenames:
        yield os.path.join(root, '.'.join([file_, ext]))
    

def connect_db(db_file, ext='sqlite'):
    """
    Establishes connection to the database file, returns connection, cursor objects and filename.
    :param db_file: Path of the database file.
    :type db_file: str/path-like object
    :param ext: extension of the database file.
        Default: sqlite
    :type ext: str
    :return: conn, cur filename
    :rtype: connection object, cursor object, str
    """
    conn = sqlite3.connect(database=db_file)
    cur = conn.cursor()
    return conn, cur, os.path.split(db_file)[1]


def database_tables(cursor):
    """
    Yields names of tables from the cursor object of the database file.
    
    Usage:
        database_tables_generator = database_tables(<cursor object>)
        name_of_ next_table = next(database_tables_generator)
    :param cursor: Cursor object attached to the database file, from connect_db function.
    :type cursor: Connection.Cursor Object
    :return: Yields table_name string in a one element tuple.
    :rtype: tuple['str']
    """
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    loop = cursor.fetchone()
    while loop is not None:
        yield loop
        loop = cursor.fetchone()
    

def table_records(cursor, table):
    """
    Yields one record (row) of the table, whenever called.
    
    Usage:
        table_records_generator = table_records(cursor, table)
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
    loop = not None
    while loop is not None:
        loop = cursor.fetchall()
        yield loop
        
    
"""
def display_results(cursor, db, tablename):
    print('=' * 50)
    print("File path: {}\nFile name: {}\nTable name: {}\n".format(*os.path.split(db), tablename))
    print('=' * 50)
    ip = input("Show all entries at once? ")
    print()
    if ip.lower() in {'yes', 'y'}:
        for row_ in cursor.fetchall():
            print(row_)
        else:
            quit()

    print("View next line: Enter", "\nTo end program: Type 'quit' without quotes and press Enter\n")
    ip = ''
    row = not None


    while ip == '' and row is not None:
        row = cursor.fetchone()
        print(row)
        ip = input()


def main():
    root = setup_paths()

    db_files = connect_db(root=root, files=files, ext=ext)
    for conn, cur, db_file in db_files:
        print('File:', os.path.split(db_file)[1])
        cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")

        #get_db_tables(cursor=cur)

        for table_ in cur.fetchone():
            try:
                table_
            except TypeError as excep:
                print("No table")
                continue
            else:
                print('Table:',  table_)
                print(cur.description)
                # table_ = next(get_db_tables(cursor=cur))[0]
                query = '''SELECT * FROM {}'''.format(table_)
                print(query)
                cur.execute(query)
                display_results(cursor=cur, db=db_file, tablename=table_)
"""
        
def main():
    root = setup_paths()
    for idx, file_ in enumerate(filepath(root=root)):
        conn, cur, filename = connect_db(db_file=file_)
        for table_ in database_tables(cursor=cur):
            print(table_)
            query = '''SELECT * FROM {}'''.format(table_[0])
            cur.execute(query)
            for row_ in cur.fetchone():
                print(row_)


            # while table_records(cur, table_):
            # print(i)
            # i += 1
            # for record_ in table_records(cur, table_):
            #     pass
            #     print(i)
            #     i += 1
            # print(record_)
            
            
            #     if table_ == 'moz_places':
            #         records = '__'
            #     else:
            #         records = list(table_records(cur, table_))
            #         print(table_, records)
            # print(list(records))
            # for record in records:
            #     print(table_, record)
            
            #
            # records = table_records(cur, 'moz_historyvisits')
            # print(list(records))


if __name__ == '__main__':
    main()
