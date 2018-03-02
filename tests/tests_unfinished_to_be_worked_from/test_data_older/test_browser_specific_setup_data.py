from collections import namedtuple
from pathlib import Path


home_dir = Path.home()


def data_for_firefox():
	firefox_testdata = dict.fromkeys(['defaults', 'values', 'exceps'])
	TestCase = namedtuple('TestCase', 'profiles expected')
	TestCaseDefault = namedtuple('TestCaseDefault', 'expected')
	
	firefox_testdata['defaults'] = (
		TestCaseDefault(expected=(
			{'RegularSurfing':
				 f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.sqlite',
			 'default':
				 f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\r057a01e.default\\places.sqlite',
			 'dev-edition-default':
				 f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default\\places.sqlite',
			 'kc.qubit':
				 f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\qllr6o0m.kc.qubit\\places.sqlite',
			 'test_profile0':
				 f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite',
			 'test_profile1':
				 f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite',
			 'test_profile2':
				 f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
			 },
			['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'favicon_id',
			 'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description',
			 'preview_image_url',
			 ],
			['id', 'url', 'title', 'visit_count', 'last_visit_date', 'url_hash',
			 'description', 'guid'
			 ],
			)
				),
	)
	
	firefox_testdata['values'] = (
		TestCase(profiles='test_profile0',
		         expected=(
			         {'test_profile0':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite'},
			         ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed',
			          'favicon_id',
			          'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash',
			          'description',
			          'preview_image_url',
			          ],
			         ['id', 'url', 'title', 'visit_count', 'last_visit_date', 'url_hash',
			          'description', 'guid'
			          ],
			         )
		         ),
		TestCase(profiles='gibberishprofile',
		         expected=(
			         {},
			         ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed',
			          'favicon_id',
			          'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash',
			          'description',
			          'preview_image_url',
			          ],
			         ['id', 'url', 'title', 'visit_count', 'last_visit_date', 'url_hash',
			          'description', 'guid'
			          ],
			         )
		         ),
		TestCase(profiles=[],
		         expected=(
			         {},
			         ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed',
			          'favicon_id',
			          'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash',
			          'description',
			          'preview_image_url',
			          ],
			         ['id', 'url', 'title', 'visit_count', 'last_visit_date', 'url_hash',
			          'description', 'guid'
			          ],
			         )
		         ),
		TestCase(profiles=['test_profile0', 'test_profile1'],
		         expected=(
			         {'test_profile0':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite',
			          'test_profile1':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite'},
			         ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed',
			          'favicon_id',
			          'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash',
			          'description',
			          'preview_image_url',
			          ],
			         ['id', 'url', 'title', 'visit_count', 'last_visit_date', 'url_hash',
			          'description', 'guid'
			          ],
			         )
		         ),
		TestCase(profiles=None,  # default value
		         expected=(
			         {'RegularSurfing':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.sqlite',
			          'default':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\r057a01e.default\\places.sqlite',
			          'dev-edition-default':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\vy2bqplf.dev-edition-default\\places.sqlite',
			          'kc.qubit':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\qllr6o0m.kc.qubit\\places.sqlite',
			          'test_profile0':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite',
			          'test_profile1':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite',
			          'test_profile2':
				          f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
			          },
			         ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'favicon_id',
			          'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description',
			          'preview_image_url',
			          ],
			         ['id', 'url', 'title', 'visit_count', 'last_visit_date', 'url_hash',
			          'description', 'guid'
			          ],
			         )
		         ),
		)
	
	firefox_testdata['exceps'] = (
		TestCase(profiles=123,
		         expected=TypeError),
		)
	
	return firefox_testdata


firefox_testdata = data_for_firefox()



def data_for_read_browser_database():
	TestCase = namedtuple('TestCase', 'filepaths fieldnames')
