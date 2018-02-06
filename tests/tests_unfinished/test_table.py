import pytest

from pprint import pprint

from . import test_table_data as ttd
from united_states_of_browsers.db_merge import table


@pytest.mark.parametrize(('test_case_in', 'test_case_expected'), [(test_case_in, test_case_expected)
                                                                  for test_case_in, test_case_expected
                                                                  in zip(ttd.init_testdata_input, ttd.init_testdata_expected)
                                                                  ])
def test_init(test_case_in, test_case_expected):
	actual_output = table.Table(*test_case_in)
	assert actual_output == test_case_expected


@pytest.mark.parametrize(('test_case_in', 'test_case_expected'), [(test_case_in, test_case_expected)
                                                                  for test_case_in, test_case_expected
                                                                  in zip(ttd.make_records_testdata_input, ttd.make_records_testdata_expected)
                                                                  ])
def test_make_records(test_case_in, test_case_expected):
	test_case_in.get_records()
	actual_output = set(dict(record)['url'] for record in test_case_in.records_yielder)
	assert actual_output == test_case_expected

def test_whiteboard():
	for test_case in zip(ttd.make_records_testdata_input, ttd.make_records_testdata_expected):
		print(test_case[0])
		test_case[0].get_records()
		actual = set(dict(record)['url'] for record in test_case[0].records_yielder)
		pprint(actual)
		print(test_case[1])

# test_whiteboard()
