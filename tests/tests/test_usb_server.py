from pathlib import Path

import flask
import pytest

from united_states_of_browsers.db_merge.db_search import check_fts5_installed
from united_states_of_browsers.usb_server import usb_server


@pytest.fixture()
def client():
    tests_root = flask.helpers.get_root_path('tests')
    app_root = Path(tests_root, 'AppData')
    db_name = 'searchable_db'
    db_path = Path(app_root, db_name)

    usb_server.app.config['DATABASE'] = str(db_path)
    usb_server.app.config['TESTING'] = True
    with usb_server.app.test_client() as client:
        with usb_server.app.app_context():
            usb_server.connect_db()
        yield client


@pytest.mark.skipif(not check_fts5_installed(), reason='FTS5 not installed')
def test_show_entries(client):
    rv = client.get('/')
    assert rv.data
    assert b'tessa' in rv.data
    assert b'getpocket' in rv.data


@pytest.mark.skipif(not check_fts5_installed(), reason='FTS5 not installed')
def test_search(client):
    search_args = {'query': 'circleci',
                   'date-from': '2388-07-01',
                   'date-to': '2388-09-29',
                   }
    rv = client.post('/search', data=search_args, follow_redirects=True)
    assert rv.data
    assert b'circleci.com' in rv.data

