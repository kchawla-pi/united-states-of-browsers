import pytest

from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge import db_search

from tests.data import test_db_search_data as dbs_data



root = Path(__file__).parents[1]
db_for_testing = Path.joinpath(root, 'tests', 'data', 'db_for_testing_search.sqlite')


@pytest.mark.parametrize('test_case', [test_case for test_case in dbs_data.search_testdata['keywords only']])
def test_search_keywords(test_case):
	actual_output = db_search.search(db_path=str(db_for_testing), word_query=test_case.input)
	assert test_case.expected == actual_output
	
	
if __name__ == '__main__':
	pass
	for test_case in dbs_data.search_testdata['keywords only']:
		test_search_keywords(test_case)
