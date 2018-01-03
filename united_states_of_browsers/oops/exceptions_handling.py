from pathlib import Path
from pprint import pprint

def invalid_path_in_tree(path_to_test):
	""" Accepts a path and returns the first invalid parent.
	"""
	path_to_test = Path(path_to_test)
	first_invalid_path_in_tree = [path_parent for path_parent in path_to_test.parents if not path_parent.exists()]
	return first_invalid_path_in_tree[-1] if first_invalid_path_in_tree else None


def test_path_tester():
	paths_to_test = ('C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing\\places.sqlite',)
	curr_path_to_test = paths_to_test[0]
	print(repr(invalid_path_in_tree(curr_path_to_test)))

if __name__ == '__main__':
	test_path_tester()
