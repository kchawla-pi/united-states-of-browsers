import sqlite3
import os
from pprint import pprint


def setup_profile_path(path=None, profile_name='regularSurfing'):
    try:
        profile_dir_path = os.path.realpath(os.path.expanduser(path))
    except TypeError:
        path_dirs = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
        profile_dir_path = os.path.expanduser(os.path.join(*path_dirs))
        profile_dir_path = os.path.realpath(profile_dir_path)
    
    try:
        profile_dir = [dir_.name for dir_ in os.scandir(profile_dir_path) if
                       dir_.name.lower().rfind(profile_name.lower()) == len(dir_.name) - len(
                           profile_name)]
    except (IndexError, FileNotFoundError):
        print(
            "\nERROR: Profile directory not found. \nCheck the profile directory path (given: {}) and"
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


def filepath(root, filenames=['places', 'storage'], ext='.sqlite'):
    if '__next__' in filenames.__dir__():
        return (os.path.join(root, file_) for file_ in filenames)
    ext_joiner = '' if ext[0] == '.' else '.'
    if isinstance(filenames, str):
        filenames = [filenames]
    return (os.path.join(root, ext_joiner.join([file_, ext])) for file_ in filenames)


def connect_db(db_file):
    conn = sqlite3.connect(database=db_file)
    cur = conn.cursor()
    return conn, cur, os.path.split(db_file)[1]


def database_tables(cursor):
    query = "SELECT name FROM sqlite_master WHERE type = 'table'"
    cursor.execute(query)
    for table_ in cursor:
        yield table_[0]


def table_records(cursor, table):
    query = '''SELECT * FROM {}'''.format(table)
    yield from cursor.execute(query)


def main():
    profile_path = setup_profile_path()
    database_files = get_database_files(profile_path=profile_path, ext='.sqlite')
    file_paths = filepath(root=profile_path, filenames='places')
    for idx, file_ in enumerate(file_paths):
        print('\n', '=' * 50, '\n', idx, 'Filename:', file_)
        conn, cur, filename = connect_db(db_file=file_)
        tables = database_tables(cursor=cur)
        for table_ in tables:
            print('.' * 8, 'Table name:', table_)
            skip_tables = {'moz_places', 'moz_historyvisits', 'moz_inputhistory'}
            if table_ in skip_tables:
                pass
            else:
                records = table_records(cursor=cur, table=table_)
                print(list(records))
            next(tables)
            # for record_ in records:
            #     print('\t'*2, end='')
            #     print(record_)


if __name__ == '__main__':
    main()
