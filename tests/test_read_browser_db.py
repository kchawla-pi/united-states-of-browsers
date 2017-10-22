from united_states_of_browsers.db_merge import read_browser_db
from tests.data import test_read_browser_db_data as rdb_data


@pytest.mark.parametrize(('test_case'), [test_case for test_case in rdb_data.firefox_values_testdata])
def test_firefox(test_case):
	actual_output = read_browser_db.firefox(profiles=test_case.profiles)
	assert test_case.expected == actual_output
