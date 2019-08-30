import sqlite3

from pathlib import Path

import pytest

from flask.helpers import get_root_path


@pytest.fixture(scope='session')
def tests_root():
    return get_root_path('tests')

@pytest.fixture(scope='session', autouse=True)
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


@pytest.fixture(scope='session', autouse=True)
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


@pytest.fixture(scope='session', autouse=True)
def create_fake_non_db_file(tests_root):
    fake_nondb_path = Path(tests_root, 'fake_nondb')
    fake_nondb_path.write_bytes(b'0')
    return str(fake_nondb_path)


@pytest.fixture(scope='session', autouse=True)
def create_invalid_filepath(tests_root):
    invalid_filepath = Path(tests_root, 'invalid_filepath')
    return str(invalid_filepath)

@pytest.fixture(scope='session', autouse=True)
def create_invalid_dirpath(tests_root):
    invalid_dirpath = Path(tests_root, 'unit_tests', 'test_table_JUNK', 'more_junk')
    return str(invalid_dirpath)
