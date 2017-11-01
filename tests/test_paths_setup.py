#  encoding -*-utf8-*-
"""
/UnitedStatesOfBrowsers$ pip install -e . (sudo) after setting up the packages and setup.py seems to
have ameliorated the import difficulties.
"""

import pytest

from united_states_of_browsers.db_merge import paths_setup
from tests.data import test_paths_setup_data as bs_data


@pytest.mark.parametrize('test_case', [test_case for test_case in bs_data.setup_profile_paths_testdata['values']])
def test_setup_profile_paths_values(test_case):
	actual_output = paths_setup.setup_profile_paths(browser_ref=test_case.browser_ref,
	                                                profiles=test_case.profiles)
	assert test_case.expected == actual_output


@pytest.mark.parametrize('test_case', [test_case for test_case in bs_data.setup_profile_paths_testdata['exceps']])
def test_setup_profile_paths_excep(test_case):
	with pytest.raises(test_case.expected) as excinfo:
		actual = paths_setup.setup_profile_paths(browser_ref=test_case.browser_ref,
		                                         profiles=test_case.profiles)


@pytest.mark.parametrize('test_case', [test_case for test_case in bs_data.db_filepaths_testdata['defaults']])
def test_db_filepath_defaults(test_case):
	actual_output = paths_setup.db_filepath(profile_paths=test_case.profile_paths)
	assert test_case.expected == actual_output

@pytest.mark.parametrize('test_case', [test_case for test_case in bs_data.db_filepaths_testdata['values']])
def test_db_filepath_values(test_case):
	actual_output = paths_setup.db_filepath(profile_paths=test_case.profile_paths,
	                                        filenames=test_case.filenames,
	                                        ext=test_case.ext)
	assert test_case.expected == actual_output
	
	
@pytest.mark.parametrize('test_case', [test_case for test_case in bs_data.db_filepaths_testdata['exceps']])
def test_db_filepath_excep(test_case):
	with pytest.raises(test_case.expected) as excinfo:
		actual_output = paths_setup.db_filepath(profile_paths=test_case.profile_paths,
		                                        filenames=test_case.filenames,
		                                        ext=test_case.ext)
