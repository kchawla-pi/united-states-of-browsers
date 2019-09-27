import tempfile
from pathlib import Path

import pytest
import flask

from united_states_of_browsers.usb_server import usb_server


@pytest.fixture()
def client():
    tests_root = flask.helpers.get_root_path('tests')
    db_path = Path(tests_root, 'AppData', 'searchable_db')
    usb_server.app.config['DATABASE'] = db_path
    usb_server.app.config['TESTING'] = True
    with usb_server.app.test_client() as client:
        with usb_server.app.app_context():
            usb_server.connect_db()
        yield client


def test_show_entries(client):
    rv = client.get('/')
    assert rv.data


# def test_search(client):
#     search_args = {flask.request.args["query"]: 'circleci'}
#     # flask.request.args["date-start"] =
#     rv = client.post('/search', data=search_args, follow_redirects=True)
#     assert rv.data
