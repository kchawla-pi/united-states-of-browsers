import pytest

from pathlib import Path

from tests.fixtures import get_project_root_path
from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import InvalidTableError


project_root = get_project_root_path()


def test_InvalidTableError_mozilla(tests_root):
	table_obj = Table(table='moz_places',
	          path=Path(tests_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/udd5sttq.test_profile2/places.sqlite'),
	          browser='firefox',
	          filename='places.sqlite',
	          profile='test_profile2',
	          copies_subpath=None,
	          )
	with pytest.raises(InvalidTableError):
		table_obj.make_records_yielder()

	
def test_InvalidTableError_chrome(tests_root):
	table_obj = Table(table='nonexistent_table',
	          path=Path(tests_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History'),
	          browser='chrome',
	          filename='History',
	          profile='Profile 1',
	          copies_subpath=None,
	          )
	with pytest.raises(InvalidTableError):
		table_obj.make_records_yielder()

	
def test_InvalidTableError_vivaldi(tests_root):
	table_obj = Table(table='nonexistent_table',
	          path=Path(tests_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History'),
	          browser='vivaldi',
	          filename='History',
	          profile='Default',
	          copies_subpath=None,
	          )
	with pytest.raises(InvalidTableError):
		table_obj.make_records_yielder()

	
def test_InvalidTableError_opera(tests_root):
	table_obj = Table(table='nonexistent_table',
	          path=Path(tests_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History'),
	          browser='opera',
	          filename='History',
	          profile='Opera Stable',
	          copies_subpath=None,
	          )
	with pytest.raises(InvalidTableError):
		table_obj.make_records_yielder()

	
# TableArgs(table='moz_places',
#              path=Path(
#                     'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
#                     'Firefox/Profiles/e0pj4lec.test_profile0/places.sqlite'),
#              browser='firefox',
#              filename='places.sqlite',
#              profile='test_profile0',
#              copies_subpath=None,
#
#              ),
