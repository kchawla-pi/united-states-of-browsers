from pathlib import Path

import pytest
import flask

from united_states_of_browsers.db_merge.db_merge import merge_browsers_history
from united_states_of_browsers.db_merge.db_search import check_fts5_installed
from united_states_of_browsers.usb_server import usb_server


@pytest.fixture()
def client(test_db):
    tests_root = flask.helpers.get_root_path('tests')
    app_root = Path(tests_root, 'AppData')
    db_name = 'usb_db.sqlite'
    db_path = Path(app_root, db_name)

    usb_server.app.config['DATABASE'] = db_path
    usb_server.app.config['TESTING'] = True
    with usb_server.app.test_client() as client:
        with usb_server.app.app_context():
            usb_server.connect_db()
        yield client


@pytest.mark.skipif(not check_fts5_installed())
def test_show_entries(client):
    rv = client.get('/')
    assert rv.data


# def test_search(client):
#     search_args = {flask.request.args["query"]: 'circleci'}
#     # flask.request.args["date-start"] =
#     rv = client.post('/search', data=search_args, follow_redirects=True)
#     assert rv.data
