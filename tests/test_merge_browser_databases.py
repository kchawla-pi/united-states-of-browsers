import pytest

from united_states_of_browsers.db_merge import merge_browser_databases

from tests.data import test_read_browser_db_data as rbd_data


test_profiles = ('test_profile0', 'test_profile1', 'test_profile2')
def test_merge(test_profiles):
	url_hashes, all_records = merge_browser_databases.merge(output_db='merged_test_db', profiles=test_profiles,)
	print(all_records, url_hashes, sep='\n\n')

test_merge(test_profiles)
