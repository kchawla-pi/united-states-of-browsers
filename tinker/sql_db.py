import sqlite3
import os
from collections import OrderedDict as odict
from pprint import pprint


def _profile_location(path=None):
    """
    (WIll be changed.)
    Accepts path and name for browser profile directory and creates the path to it.
    Currently, By default uses Firefox's profile path for win10 for a profile named default.
    :param path:
    :type path:
    :return:
    :rtype:
    """
    try:
        profile_loc = os.path.realpath(os.path.expanduser(path))
    except TypeError:
        path_dirs = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
        profile_loc = os.path.expanduser(os.path.join(*path_dirs))
        profile_loc = os.path.realpath(profile_loc)
    return profile_loc


def _profile_dir(profile_loc, *, profile_name=None):
    """
    Finds the names of all profile directories (default) or for specified profile.
    :param profile_loc:
    :type profile_loc:
    :param profile_name:
    :type profile_name:
    :return:
    :rtype:
    """
    if not profile_name:
        return [dir_.name for dir_ in os.scandir(profile_loc)]
    try:
        profile_dir_ = [dir_.name for dir_ in os.scandir(profile_loc) if
                        dir_.name.lower().rfind(profile_name.lower()) == len(dir_.name) - len(
                                    profile_name)]
    except (IndexError, FileNotFoundError):
        print(
                    "\nERROR: Profile directory not found. \nCheck the profile directory path (given: {}) and"
                    " profile name string (given: {}).".format(profile_loc, profile_name))
    else:
        return profile_dir_


def _setup_profile_paths(profile_loc, profile_dir_names):
    return [os.path.join(profile_loc, profile_dir_) for profile_dir_ in profile_dir_names]


def _setup_paths(path=None):
    """
    Sets up the directory path for sqlite database files.
    Returns path to sqlite file's copy stored in project directory.
    :return: root directory
    :rtype: str/path-like object
    """
    profile_loc = _profile_location(path)
    profile_dir_names = _profile_dir(profile_loc, profile_name='regularSurfing')
    profile_paths = _setup_profile_paths(profile_loc, profile_dir_names)
    return profile_paths


def _db_files(root, ext='.sqlite'):
    """
    Returns a list of file in the specified directory (not subdirectories) with a specified (or no) extension.
    :param root: Path to directory with the files
    :type root: str/path-like object
    :param ext: Extension for the file. (Default: .sqlite)
    :type ext: str | None
    :return: list of files with the specified extension.
    :rtype: list[str]
    """
    if root is None or os.path.exists(root) is False:
        print("ERROR: Path was not found (given: {})".format(root))
        return
    try:
        for curr_dir, subdirs, files in os.walk(root):
            break
    except TypeError:
        print("ERROR: Path can not be None")
    else:
        ext = ext[1:] if ext[0] == '.' else ext
        return [file_ for file_ in files if file_.rfind(ext) == len(file_) - len(ext)]


def _filepath(root, filenames=None, ext='sqlite'):
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
    try:
        ext_joiner = '' if ext[0] in {os.extsep, '.'} else os.extsep
    except (TypeError, IndexError):
        ext_joiner = ''
        ext = ''
    if isinstance(filenames, str):
        filenames = [filenames]
    elif filenames is None:
        filenames = _db_files(root=root, ext=ext)
    try:
        # [os.path.join(root_, ext_joiner.join([file_, ext])) for file_ in filenames for root_ in root]
        file_names = [ext_joiner.join([file_, ext]) for file_ in filenames]
        return [os.path.join(root_, file_name_) for root_ in root for file_name_ in file_names]
    except TypeError as excep:
        print("ERROR: Invalid parameters in function _filepath().")
        print(excep)


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
    profile_paths = _setup_paths()
    file_paths = _filepath(root=profile_paths, filenames='places', ext='sqlite')
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
    file_paths = _filepath(
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
