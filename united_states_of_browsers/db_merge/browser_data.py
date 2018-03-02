from collections import namedtuple
from pathlib import Path

BrowserData = namedtuple('BrowserData', 'os browser path profiles file_tables table_fields')


def prep_browsers_info(parent_dir='~'):
	parent_dir = Path(parent_dir)
	return [BrowserData(os='nt',
	                    browser='firefox',
	                    path=parent_dir.joinpath('AppData','Roaming','Mozilla','Firefox','Profiles'),
	                    profiles=None,
	                    file_tables={'places.sqlite': ['moz_places']},
	                    table_fields={'moz_places': ['id', 'url', 'title', 'visit_count', 'last_visit_date',
	                                                 'last_visit_readable']},
	                    ),
	        BrowserData(os='nt',
	                    browser='chrome',
	                    path=parent_dir.joinpath('AppData','Local','Google','Chrome','User Data'),
	                    profiles=None,
	                    file_tables={'history': ['urls']},
	                    table_fields={'urls': ['id', 'url', 'title', 'visit_count', 'last_visit_time',
	                                           'last_visit_readable']},
	                    ),
	        BrowserData(os='nt',
	                    browser='opera',
	                    path=parent_dir.joinpath('AppData','Roaming','Opera Software'),
	                    profiles=None,
	                    file_tables={'History': ['urls']},
	                    table_fields={'urls': ['id', 'url', 'title', 'visit_count', 'last_visit_time',
	                                           'last_visit_readable']},
	                    ),
	        BrowserData(os='nt',
	                    browser='vivaldi',
	                    path=parent_dir.joinpath('AppData','Local','Vivaldi','User Data'),
	                    profiles=None,
	                    file_tables={'History': ['urls']},
	                    table_fields={'urls': ['id', 'url', 'title', 'visit_count', 'last_visit_time',
	                                           'last_visit_readable']},
	                    ),
	        ]


history_table_fieldnames = ['id', 'url', 'title', 'visit_count', 'last_visit', 'last_visit_readable', 'browser',
                            'profile', 'file', 'tablename']
search_table_fields = ['rec_id', 'id', 'url', 'title', 'visit_count', 'last_visit', 'last_visit_readable', 'browser',
                       'profile', 'file',
                       'tablename']


if __name__ == '__main__':
	from pathlib import Path
	from pprint import pprint
	
	
	# pprint(prep_browsers_info())
	
	new_parent = Path(__file__).parents[2].joinpath('tests', 'data', 'browser_profiles_for_testing')
	print(new_parent)
	print(new_parent, 'aba')
	pprint(prep_browsers_info(new_parent))
