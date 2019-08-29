import pytest

from collections import namedtuple
from pathlib import Path

from tests.fixtures import get_project_root_path
from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import InvalidTableError


project_root = get_project_root_path()

TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath')
test_cases_exception_InvalidTableError = [
	TableArgs(table='moz_places',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/udd5sttq.test_profile2/places.sqlite'),
	          browser='firefox',
	          filename='places.sqlite',
	          profile='test_profile2',
	          copies_subpath=None,
	          ),
	TableArgs(table='nonexistent_table',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History'),
	          browser='chrome',
	          filename='History',
	          profile='Profile 1',
	          copies_subpath=None,
	          ),
	TableArgs(table='nonexistent_table',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History'),
	          browser='vivaldi',
	          filename='History',
	          profile='Default',
	          copies_subpath=None,
	          ),
	TableArgs(table='nonexistent_table',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History'),
	          browser='opera',
	          filename='History',
	          profile='Opera Stable',
	          copies_subpath=None,
	          ),
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
	]


@pytest.mark.parametrize('test_case', [test_case for test_case in test_cases_exception_InvalidTableError])
def test_suite_no_such_table(test_case):
	table_obj = Table(*test_case)
	with pytest.raises(InvalidTableError):
		table_obj.make_records_yielder()


def non_pytest_test_suite_no_such_table(test_suite):
	for test_case in test_suite:
		table_obj = Table(*test_case)
		try:
			table_obj.make_records_yielder()
		except InvalidTableError:
			print('Passed.')


if __name__ == '__main__':
	non_pytest_test_suite_no_such_table(test_suite=test_cases_exception_InvalidTableError)
