import pytest

from pprint import pprint

from united_states_of_browsers.oops import table
from united_states_of_browsers.oops import test_table_data as ttd


@pytest.mark.parametrize('test_case', [test_case for test_case in zip(ttd.table_testdata_input, ttd.table_testdata_expected)])
def test_firefox(test_case):
	actual_output = table.Table(*test_case[0])
	assert actual_output == test_case[1]
