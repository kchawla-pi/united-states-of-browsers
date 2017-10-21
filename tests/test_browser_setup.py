# from pathlib import Path
# import sys
# search_path = str(Path(__file__).parents[1])
# print(f'Adding {search_path} to PYTHONPATH')
#
# try:
# 	import pytest
# except ImportError:
# 	sys.path.insert(0, search_path)
# 	import pytest

"""
/UnitedStatesOfBrowsers$ pip install -e . (sudo) after setting up the packages and setup.py seems to
have ameliorated the import difficulties.
"""

import pytest
import hypothesis

from united_states_of_browsers.db_merge import browser_setup
from tests.data import test_browser_setup_data as bs_data


collected_tests = []

@pytest.mark.parametrize(('test_case'), [test_case for test_case in bs_data.setup_profile_paths])
def test_setup_profile_paths(test_case):
	global collected_tests
	try:
		actual_output = browser_setup.setup_profile_paths(browser_ref=test_case.browser_ref, profiles=test_case.profiles)
	except Exception as excep:
		actual_output = str(excep)
	assert test_case.expected == actual_output
	collected_tests.append((test_case),)


# def test_db_filepath(test_input):
# 	try:
# 		actual_output = browser_setup.db_filepath(
	
if __name__ == '__main__':
	pytest.main()

