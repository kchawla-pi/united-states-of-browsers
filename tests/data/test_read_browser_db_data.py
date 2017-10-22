from collections import namedtuple
from pathlib import Path


home_dir = Path.home()

def data_for_firefox():
	TestCase = namedtuple('TestCase', 'profiles expected')
	
	firefox_values_testdata = (
		TestCase(profiles='test_profile0',
		         expected=(
			         {'test_profile0':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite'},
			         ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'favicon_id',
			          'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description',
			          'preview_image_url',]
			         ),
		         ),
		)
	
	return firefox_values_testdata

firefox_values_testdata = data_for_firefox()
