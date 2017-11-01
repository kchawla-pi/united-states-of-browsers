import pytest

from united_states_of_browsers.db_merge import browser_specific_setup
from tests.data import test_browser_specific_setup_data as bss_data


@pytest.mark.parametrize('test_case', [test_case for test_case in bss_data.firefox_testdata['defaults']])
def test_firefox_defaults(test_case):
	actual_output = browser_specific_setup.firefox()
	assert test_case.expected == actual_output

@pytest.mark.parametrize('test_case', [test_case for test_case in bss_data.firefox_testdata['values']])
def test_firefox_values(test_case):
	actual_output = browser_specific_setup.firefox(profiles=test_case.profiles)
	assert test_case.expected == actual_output

@pytest.mark.parametrize('test_case', [test_case for test_case in bss_data.firefox_testdata['exceps']])
def test_firefox_excep(test_case):
	with pytest.raises(test_case.expected) as excinfo:
		actual_output = browser_specific_setup.firefox(profiles=test_case.profiles)

