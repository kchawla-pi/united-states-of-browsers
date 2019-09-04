import os
import sqlite3

from pathlib import Path

import pytest

from flask.helpers import get_root_path


@pytest.fixture(scope='session')
def tests_root():
    return get_root_path('tests')

@pytest.fixture(autouse=True)
def create_mozilla_data(tmpdir):
    db_path = str(Path(tmpdir, 'test_mozilla.sqlite'))
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                '''CREATE TABLE IF NOT EXISTS moz_places ( id INTEGER, url LONGVARCHAR, title LONGVARCHAR, rev_host LONGVARCHAR, visit_count INTEGER DEFAULT 0, hidden INTEGER DEFAULT 0 NOT NULL, typed INTEGER DEFAULT 0 NOT NULL, frecency INTEGER DEFAULT -1 NOT NULL, last_visit_date INTEGER , guid TEXT, foreign_count INTEGER DEFAULT 0 NOT NULL, url_hash INTEGER DEFAULT 0 NOT NULL , description TEXT, preview_image_url TEXT, origin_id INTEGER REFERENCES moz_origins(id))'''
                    )
        except sqlite3.OperationalError:
            pass
        cur.execute(
                '''INSERT INTO moz_places VALUES ("13",	"https://www.linuxmint.com/start/tessa/", "Start Page - Linux Mint", "moc.tnimxunil.www.", "7", "0", "0", "37", "1547771594938637", "FJ1OyVWgG0Zb", "0", "47360064011053", "", "", "8")'''
                )
        cur.execute(
                '''INSERT INTO moz_places VALUES("1", "https://support.mozilla.org/en-US/products/firefox", " ",  "gro.allizom.troppus.", "0", "0", "0", "20", " ", "OH2P1G22WscA", "1", "47357795150914", "", "", "1")'''
                )
        cur.execute(
                '''INSERT INTO moz_places VALUES("1", "https://support.mozilla.org/en-US/products/firefox", " ",  "gro.allizom.troppus.", "0", "0", "0", "20", " ", "OH2P1G22WscA", "1", "478687686807678876867357795150914", "", "", "1")'''
                )
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
                '''CREATE TABLE IF NOT EXISTS moz_origins ( id INTEGER, prefix TEXT NOT NULL, host TEXT NOT NULL, frecency INTEGER NOT NULL)'''
                )
        cur.execute(
                '''INSERT INTO moz_origins VALUES("1", "https://", "support.mozilla.org", "280")'''
                )

    return db_path


@pytest.fixture(autouse=True)
def create_chromium_data(tmpdir):
    db_path = str(Path(tmpdir, 'test_chromium'))
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS urls(id INTEGER, url LONGVARCHAR,title LONGVARCHAR,visit_count INTEGER DEFAULT 0 NOT NULL,typed_count INTEGER DEFAULT 0 NOT NULL,last_visit_time INTEGER NOT NULL,hidden INTEGER DEFAULT 0 NOT NULL)'''
                )
        cur.execute(
                '''INSERT INTO urls VALUES ("88", "https://www.google.com/search?q=chrome+linux+profile+data&oq=chrome+linux+profile+data&aqs=chrome..69i57j33l4.3443j0j7&sourceid=chrome&ie=UTF-8", "chrome linux profile data - Google Search", "1", "0", "13204503690648295", "0")'''
                )
    return db_path


@pytest.fixture(autouse=True)
def create_fake_non_db_file(tmpdir):
    fake_nondb_path = Path(tmpdir, 'fake_nondb')
    fake_nondb_path.write_bytes(b'0')
    return str(fake_nondb_path)


@pytest.fixture(autouse=True)
def create_invalid_filepath(tmpdir):
    invalid_filepath = Path(tmpdir, 'invalid_filepath')
    return str(invalid_filepath)
