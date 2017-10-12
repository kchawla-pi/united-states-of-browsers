import sqlite3
import os
from time import sleep
from pprint import pprint


def setup_profile_path(path=None, profile_name='regularSurfing' ):
    try:
        profile_dir_path = os.path.realpath(os.path.expanduser(path))
    except TypeError:
        path_dirs = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
        profile_dir_path = os.path.expanduser(os.path.join(*path_dirs))
        profile_dir_path = os.path.realpath(profile_dir_path)
    
    try:
        profile_dir = [dir_.name for dir_ in os.scandir(profile_dir_path) if dir_.name.lower().rfind(profile_name.lower()) == len(dir_.name) - len(profile_name)]
    except (IndexError, FileNotFoundError):
        print("\nERROR: Profile directory not found. \nCheck the profile directory path (given: {}) and"
        " profile name string (given: {}).".format(profile_dir_path, profile_name))
    else:
        return os.path.join(profile_dir_path, *profile_dir)
    
    
def get_database_files(profile_path, ext='.sqlite'):
    if profile_path is None or os.path.exists(profile_path) is False:
        print("ERROR: Path was not found (given: {})".format(profile_path))
        return
    try:
        for curr_dir, subdirs, files in os.walk(profile_path):
            break
    except TypeError:
        print("ERROR: Path can not be None")
    else:
        try:
            return (file_ for file_ in files if file_.rfind(ext) == len(file_) - len(ext))
        except StopIteration as excep:
            return False
        except TypeError:
            return False


def setup_paths():
    """
    Sets up the directory path for sqlite database files"
    :return: root directory
    :rtype: str/path-like object
    """
    return os.path.realpath(os.path.join(os.path.split(__file__)[0],
                                         'data', 'firefox_regular_surfing')
                            )


def filepath(root, filenames= ['places', 'storage'], ext='.sqlite'):
    """
    Yields the path for the next database file.
    By default, these are sqlite file. (used by browsers to store history, bookmarks etc)
    
    Usage:
        filepath_generator = _filepath(root, filenames, ext)
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
    if '__next__' in filenames.__dir__():
        return (os.path.join(root, file_) for file_ in filenames)
    ext_joiner = '' if ext[0] == '.' else '.'
    if isinstance(filenames, str):
        filenames = [filenames]
    return (os.path.join(root, ext_joiner.join([file_, ext])) for file_ in filenames)
    

def connect_db(db_file):
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
        database_tables_generator = _db_tables(<cursor object>)
        name_of_ next_table = next(database_tables_generator)
    :param cursor: Cursor object attached to the database file, from connect_databases function.
    :type cursor: Connection.Cursor Object
    :return: Yields table_name string in a one element tuple.
    :rtype: tuple['str']
    """
    query = "SELECT name FROM sqlite_master WHERE type = 'table'"
    cursor.execute(query)
    for table_ in cursor:
        yield table_[0]
    

def table_records(cursor, table):
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
    if '__next__' in table.__dir__():
        return (cursor.execute('''SELECT * FROM {}'''.format(table)) for table_ in table)
        
    query = '''SELECT * FROM {}'''.format(table)
    cursor.execute(query)
    for record_ in cursor:
        yield record_, cursor.description
    # yield from cursor
    # return cursor.description
    
    
def prep_records(records_generator):
    record_dict = []
    for record_, desc in records_generator:
        pass
        # if record_[0] == 1:
        field_names = [desc_[0] for desc_ in desc]
            # yield ({field_name_: field_ for field_name_, field_ in zip(field_names, record_)})
        record_dict.append(
                    {field_name_: field_ for field_name_, field_ in zip(field_names, record_)}
                    )
        # for record_dict
        pprint(record_dict)


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


def write_to_db():
    root = setup_profile_paths()

    db_files = connect_databases(root=root, files=files, ext=ext)
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
    profile_path = setup_profile_path()
    database_files = get_database_files(profile_path=profile_path, ext='.sqlite')
    file_paths = filepath(root=profile_path, filenames='places')
    for idx, file_ in enumerate(file_paths):
        print('\n', '='*50, '\n', idx, 'Filename:', file_)
        conn, cur, filename = connect_db(db_file=file_)
        tables = database_tables(cursor=cur)
        for table_ in tables:
            print('.'*8, 'Table name:', table_)
            conn, cur, filename = connect_db(db_file=file_)
            records = table_records(cursor=cur, table=table_)
            prepped_records = prep_records(records)
            # for record_ in prepped_records:
            #     pprint(record_)
        quit()
            

if __name__ == '__main__':
    main()

