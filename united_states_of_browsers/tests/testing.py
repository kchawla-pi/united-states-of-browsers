# -*- encoding: utf-8 -*-
from pprint import pprint

from oops.new_browser_setup import Browser
from oops.database_file import DBFile
from oops.database_table import Table

def fx_test():
	profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	firefox = Browser('firefox', profile_pathcrumbs_firefox, ['places.sqlite'])
	firefox.setup_paths()
	pprint(firefox.profile_paths)
	current_path = firefox.profile_paths
	# db_file0 = DBFile(current_path)

if __name__ == '__main__':
	fx_test()
