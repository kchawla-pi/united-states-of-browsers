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


@pytest.mark.parametrize(('test_input', 'expected_output'), [(input_data, expected_output)
                                                             for input_data, expected_output
                                                             in bs_data.setup_profile_paths.items()
                                                             ])
def test_setup_profile_paths(test_input, expected_output ):
	try:
		actual_output = browser_setup.setup_profile_paths(browser_ref=test_input.browser_ref, profiles=test_input.profiles)
	except Exception as excep:
		actual_output = str(excep)
	assert expected_output == actual_output


	
if __name__ == '__main__':
	pytest.main()

