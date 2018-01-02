import pytest

from pprint import pprint

from united_states_of_browsers.oops import table
from united_states_of_browsers.oops import test_table_data as ttd


@pytest.mark.parametrize('test_case', [test_case for test_case in zip(ttd.init_testdata_input, ttd.init_testdata_expected)])
def test_firefox_init(test_case):
	actual_output = table.Table(*test_case[0])
	assert actual_output == test_case[1]

@pytest.mark.parametrize('test_case', [test_case for test_case in zip(ttd.make_records_testdata_input, ttd.make_records_testdata_expected)])
def test_firefox_make_records(test_case):
	test_case[0].get_records()
	actual_output = [dict(record)['url'] for record in test_case[0].records_yielder]
	assert actual_output == ttd.make_records_testdata_expected
