import sqlite3
import os
from pprint import pprint


def setup_paths():
    """
    Sets up the directory path, filenames and extensions for sqlite database files"
    :return: root directory, file list, extension
    :rtype: str/path-like object, list(str), str
    """
    root = os.path.realpath(os.path.join(
                os.path.split(__file__)[0], 'data', 'firefox_regular_surfing'
                )
                )
    files = ['places', 'storage']
    ext = 'sqlite'
    return root, files, ext


def connect_db(root, files, ext='sqlite'):
    db_files = (os.path.join(root, '.'.join([file_, ext])) for file_ in files)
    
    db_file = next(db_files)
    conn = sqlite3.connect(database=db_file)
    cur = conn.cursor()
    yield conn, cur, db_file
    

def get_db_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    yield cursor.fetchone()
    
    
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
    root, files, ext = setup_paths()
    db_info = connect_db(root=root, files=files, ext=ext)
    for conn, cur, db_file in db_info:
        table_ = next(get_db_tables(cursor=cur))[0]
        query = '''SELECT * FROM {}'''.format(table_)
        cur.execute(query)
        display_results(cursor=cur, db=db_file, tablename=table_)
        
        
    

if __name__ == '__main__':
    main()
