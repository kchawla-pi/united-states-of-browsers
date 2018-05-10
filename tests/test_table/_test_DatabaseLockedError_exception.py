from pprint import pprint

import pytest
import sqlite3

from collections import namedtuple
from pathlib import Path

from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import DatabaseLockedError


project_root = Path(__file__).parents[2]

TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath')
test_cases_exception_DatabaseLockedError = [
	TableArgs(table='urls',
	             path=Path(project_root,
			             'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History'),
	             browser='chrome',
	             filename='History',
	             profile='Profile 1',
	             copies_subpath=None,
	             ),
	TableArgs(table='urls',
	             path=Path(project_root,
			             'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History'),
	             browser='vivaldi',
	             filename='History',
	             profile='Default',
	             copies_subpath=None,
	             ),
	TableArgs(table='urls',
	             path=Path(project_root,
			             'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History'),
	             browser='opera',
	             filename='History',
	             profile='Opera Stable',
	             copies_subpath=None,
	             ),
	TableArgs(table='moz_places',
	             path=Path(project_root,
			             'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
			             'Firefox/Profiles/e0pj4lec.test_profile0/places.sqlite'),
	             browser='firefox',
	             filename='places.sqlite',
	             profile='test_profile0',
	             copies_subpath=None,
	             ),
	TableArgs(table='moz_places',
	             path=Path(project_root,
			             'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
			             'Firefox/Profiles/kceyj748.test_profile1/places.sqlite'),
	             browser='firefox',
	             filename='places.sqlite',
	             profile='test_profile1',
	             copies_subpath=None,
	             ),
	
	]


@pytest.mark.parametrize('test_case', [test_case for test_case in test_cases_exception_DatabaseLockedError])
def test_DatabaseLockedError(test_case):
	pass


def non_pytest_test_DatabaseLockedError(test_suite):
	for test_case in test_suite:
		db_file_path_uri_mode = f'file:{test_case.path}?mode=ro'
		conn = sqlite3.connect(f'{test_case.path}', isolation_level='EXCLUSIVE')
		# conn.row_factory = sqlite3.Row'
		cur = conn.cursor()
		yield_records = cur.execute(f'SELECT * FROM {test_case.table}')
		pprint(list(yield_records))
		# with sqlite3.connect(f'{test_case.path}') as conn2:
		# 	conn
		table_obj = Table(*test_case)
		table_obj._connect()
		# table_obj.make_records_yielder()

if __name__ == '__main__':
	non_pytest_test_DatabaseLockedError(test_suite=test_cases_exception_DatabaseLockedError)
	
