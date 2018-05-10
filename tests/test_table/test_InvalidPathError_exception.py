import pytest
import sqlite3

from collections import namedtuple
from pathlib import Path

from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import InvalidPathError


project_root = Path(__file__).parents[2]

TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath')
test_cases_exception_InvalidPathError = [
	TableArgs(table='moz_places',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing_wrongpath_/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/kceyj748.test_profile1/places.sqlite'),
	          browser='firefox',
	          filename='places.sqlite',
	          profile='test_profile1',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1 _wrongpath_/History'),
	          browser='chrome',
	          filename='History',
	          profile='Profile 1 _wrongpath_',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User_wrongpath_ Data/Default/History'),
	          browser='vivaldi',
	          filename='History',
	          profile='Default',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData_wrongpath_/Roaming/Opera Software/Opera Stable/History'),
	          browser='opera',
	          filename='History',
	          profile='Opera Stable',
	          copies_subpath=None,
	          ),
	]


@pytest.mark.parametrize('test_case', [test_case for test_case in test_cases_exception_InvalidPathError])
def test_InvalidPathError(test_case):
	table_obj = Table(*test_case)
	with pytest.raises(OSError) as excep:
		table_obj.make_records_yielder()


def non_pytest_test_InvalidPathError(test_suite):
	for test_case in test_suite:
		table_obj = Table(*test_case)
		try:
			table_obj.make_records_yielder()
			pass
		except InvalidPathError as excep:
			print(f'Expected Exception raised', excep, '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
		except Exception as excep:
			raise excep
		else:
			print(f'Expected Exception NOT raised', '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
			raise Exception('Expected exception not raised.')
		finally:
			print()
			
			
if __name__ == '__main__':
	non_pytest_test_InvalidPathError(test_suite=test_cases_exception_InvalidPathError)
	# for test_case in test_cases_exception_InvalidFileError:
	# 	table_obj = Table(*test_case)
	# 	table_obj.make_records_yielder()

