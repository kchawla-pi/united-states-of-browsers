
from oops.browser_setup import Browser
from oops.database_file import DBFile
from oops.database_table import Table

def fx_test():
	profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	firefox = Browser('firefox', profile_pathcrumbs_firefox, ['places.sqlite'])
	firefox.setup_paths()
	print(firefox)


if __name__ == '__main__':
	fx_test()
