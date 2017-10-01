from collections import OrderedDict as odict

import write_new_db



def create_test_data():
	test_record = odict(
				{'id': 1, 'url': 'https://www.mozilla.org/en-US/firefox/central/', 'title': None,
				 'rev_host': 'gro.allizom.www.', 'visit_count': 0, 'hidden': 0, 'typed': 0,
				 'favicon_id': None, 'frecency': 76, 'last_visit_date': None, 'guid': 'NNqZA_f2KHI1',
				 'foreign_count': 1, 'url_hash': 47356370932282, 'description': None,
				 'preview_image_url': None
				 })
	return test_record

if __name__ == '__main__':
	test_record = create_test_data()
	write_new_db.write_to_db(database='test.sqlite', record=test_record)
