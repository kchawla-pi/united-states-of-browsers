# -*- encoding: utf-8 -*-
from united_states_of_browsers.db_merge import browser_setup

from united_states_of_browsers.db_merge.imported_annotations import *


def firefox(profiles: Optional[Union[Text, Sequence[Text]]]=None) -> Tuple[List[PathInfo], List[Text]]:
	'''
	Setups path & field names of places.sqlite file for Firefox browser profiles in Windows x64.
	Returns all profiles by default.
	Optionally, Accepts profile name or list of profile names.
	Returns tuple of list of Paths and field_names
	'''
	firefox_fieldnames = ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed',
	                       'favicon_id', 'frecency', 'last_visit_date', 'guid', 'foreign_count',
	                       'url_hash', 'description', 'preview_image_url',
	                       ]
	profile_paths = browser_setup.setup_profile_paths(browser_ref='firefox', profiles=profiles)
	file_paths = browser_setup.db_filepath(profile_paths=profile_paths, filenames='places', ext='sqlite')
	return file_paths, firefox_fieldnames


def chrome():
	home_dir = Path.home()
	file_paths = browser_setup.db_filepath(
				root=f'{home_dir}\\AppData\\Local\\Google\\Chrome\\User Data\\Default',
				filenames='History', ext=None)
	

if __name__ == '__main__':
	profiles = ['RegularSurfing', 'default', 'dev-edition-default']
	# firefox(['test_profile0'])
	filepaths = firefox('default')
