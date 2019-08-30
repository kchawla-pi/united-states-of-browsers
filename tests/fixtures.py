import sqlite3
from pathlib import Path

from united_states_of_browsers.db_merge import helpers


def get_project_root_path():
    project_dirnames = ['UnitedStatesOfBrowsers',
                        'united-states-of-browsers',
                        ]
    for dirname in project_dirnames:
        try:
            project_root = helpers.get_root_path(
                    project_file_path=__file__,
                    project_root_dir_name=dirname,
                    )
        except ValueError:
            pass
        else:
            break
    else:
        raise ValueError(
                f'Project directory name not in list {project_dirnames}'
                )
    return project_root


def create_mozilla_data(tests_root):
    db_path = str(Path(tests_root, 'test_mozilla.sqlite'))
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute(
            '''CREATE TABLE moz_places ( id INTEGER PRIMARY KEY, url LONGVARCHAR, title LONGVARCHAR, rev_host LONGVARCHAR, visit_count INTEGER DEFAULT 0, hidden INTEGER DEFAULT 0 NOT NULL, typed INTEGER DEFAULT 0 NOT NULL, frecency INTEGER DEFAULT -1 NOT NULL, last_visit_date INTEGER , guid TEXT, foreign_count INTEGER DEFAULT 0 NOT NULL, url_hash INTEGER DEFAULT 0 NOT NULL , description TEXT, preview_image_url TEXT, origin_id INTEGER REFERENCES moz_origins(id))'''
                )
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute(
                '''INSERT INTO moz_places VALUES ("13",	"https://www.linuxmint.com/start/tessa/", "Start Page - Linux Mint", "moc.tnimxunil.www.", "7", "0", "0", "37", "1547771594938637", "FJ1OyVWgG0Zb", "0", "47360064011053", "", "", "8")'''
                )
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()
    return db_path

def create_chromium_data(tests_root):
    db_path = str(Path(tests_root, 'test_chromium'))
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute(
            '''CREATE TABLE urls(id INTEGER PRIMARY KEY AUTOINCREMENT,url LONGVARCHAR,title LONGVARCHAR,visit_count INTEGER DEFAULT 0 NOT NULL,typed_count INTEGER DEFAULT 0 NOT NULL,last_visit_time INTEGER NOT NULL,hidden INTEGER DEFAULT 0 NOT NULL)'''
                )
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute(
                '''INSERT INTO urls VALUES ("88", "https://www.google.com/search?q=chrome+linux+profile+data&oq=chrome+linux+profile+data&aqs=chrome..69i57j33l4.3443j0j7&sourceid=chrome&ie=UTF-8", "chrome linux profile data - Google Search", "1", "0", "13204503690648295", "0")'''
                )
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()
    return db_path
