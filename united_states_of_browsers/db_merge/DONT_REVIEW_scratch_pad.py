'''
A place for experimentation and playing with new concepts and ideas. Not included in the actual finished code.
'''
"""
keys = {
	8470: ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'favicon_id',
	       'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description',
	       'preview_image_url'],
	8471: ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'favicon_id',
	       'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description',
	       'preview_image_url'],
	8472: ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'frecency',
	       'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description',
	       'preview_image_url'],
		
	}

import os


filepath_from_another = lambda *filename, filepath=__file__: os.path.realpath(
	os.path.join(os.path.dirname(filepath), *filename))
import sqlite3


print(filepath_from_another('output', 'abc.txt'))
print(filepath_from_another('output', 'try', 'abc.txt'))
print(filepath_from_another('output', 'try', 'abc.txt', filepath='C:'))
from pathlib import Path


def fpfa(filepath=__file__, *filename):
	filepath_dir = os.path.dirname(filepath)
	filepath = os.path.join(*filepath)
	return os.path.realpath(os.path.join(filepath_dir, filepath))


print()
print(fpfa())
print(fpfa('abc.txt'))
print(fpfa('output', 'abc.txt'))
print()
db_file = Path(os.path.dirname(__file__), 'merged_fx_db.sqlite')

filepath_from_another = lambda filepath=__file__, *filename: os.path.realpath(
	os.path.join(os.path.dirname(filepath), *tuple(filename)))

# print(filepath_from_another())
print(filepath_from_another('abc.txt'))
print(filepath_from_another('output', 'abc.txt'))
# print(filepath_from_another('output', 'try', 'abc.txt', filepath='C:'))

# conn =
with sqlite3.connect(str(db_file)) as conn:
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	query = '''SELECT * FROM moz_places'''
	cur.execute(query)
	for row in cur:
		print(row)
		print(dict(row))
	
	# conn.close()
def scratch_pad2():
	import sqlite3
	
	from db_merge.helpers import filepath_from_another
	
	db_path = filepath_from_another('test3.sqlite')
	
	conn = sqlite3.connect(db_path)
	cur = conn.cursor()
	
	query = 'SELECT * FROM moz_places ORDER BY url_hash'
	cur.execute(query)
	
	for record in cur:
		print(record)
"""
"""
import os
import setuptools

packages_dir={'':'united_states_of_browsers'}

print(os.getcwd())
package_list = setuptools.find_packages('./united_states_of_browsers')
print(package_list)
"""
"""
from db_merge.browser_setup import setup_profile_paths

# test_args = [('', ''), ('somegibberish', 'somemoregibberish'), ('somegibberish', None), (123, 321)]
test_args = [('Firefox', ['regular_surfing', 'default'])]
for browser_ref, profiles in test_args:
	try:
		actual_output = (setup_profile_paths(browser_ref=browser_ref, profiles=profiles))
	except Exception as excep:
		actual_output = str(excep)
	print('input:', browser_ref, profiles, 'output:', actual_output, type(actual_output))
"""
"""
import types

proxy_map = types.MappingProxyType({'a': 1, 'b': 2})
print(proxy_map)


from collections import namedtuple

ReplaceDict = namedtuple('ReplaceDict', 'input expected')

replaced_dict = ReplaceDict(input='a', expected={})
print(replaced_dict)
# for item1, item2 in replaced_dict.items():
"""
"""
import pytest

from pathlib import Path
from pprint import pprint
from db_merge import browser_setup

home_dir = Path.home()
with pytest.raises(AttributeError) as excinfo:
	actual = browser_setup.db_filepath(
			profile_paths=123,
			filenames='places', ext='.sqlite')

	pprint(actual)
"""

"""
import pytest

from pathlib import Path
from pprint import pprint
from db_merge import read_browser_db

home_dir = Path.home()
with pytest.raises(AttributeError) as excinfo:
	actual = read_browser_db.firefox(profiles=[])
	pprint(actual)
"""

from pprint import pprint
from db_merge import read_browser_db
pprint(read_browser_db.firefox(profiles={}))
