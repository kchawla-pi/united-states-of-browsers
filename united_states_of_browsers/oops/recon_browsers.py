import sqlite3

from pathlib import Path
from pprint import pprint


def print_objects(objects_list):
	for obj in objects_list:
		print('repr:', repr(obj))
		pprint(obj)
		print('-' * 25)

def get_tablenames(path):
	path = Path(path)
	with sqlite3.connect(str(path)) as conn:
		cur = conn.cursor()
		query = 'SELECT name FROM sqlite_master where type == "table"'
		query_result = cur.execute(query)
		return {(path.parents[0].name, path.name): [result[0] for result in query_result]}

def get_fieldnames(path, table):
	path = Path(path)
	with sqlite3.connect(str(path)) as conn:
		cur = conn.cursor()
		query = f'SELECT * FROM {table}'
		cur.execute(query)
		return {(path.parents[0].name, path.name, table): [fieldname[0] for fieldname in cur.description]}

def get_sqlite_files(path):
	path = Path(path)
	# print(path.name)
	return [entry for entry in path.iterdir() if not entry.is_dir() and '.sqlite' in entry.name]

def print_tables(table_yielders):
	for tablename, table in table_yielders.items():
		try:
			print(tablename, ':', list(dict(table.records_yielder.fetchone()).keys()))
			# for record in table.records_yielder:
			# 	print(dict(record), '\n')
		except (TypeError, AttributeError) as excep:
			pass
			# print('No records retrieved.')

def recon_firefox():
	path = 'C:/Users/kshit/AppData/Roaming/Mozilla/Firefox/Profiles/e0pj4lec.test_profile0/'
	pprint(get_tablenames(path + 'favicons.sqlite'))
	pprint(get_fieldnames(path + 'favicons.sqlite', 'moz_icons'))
	quit()

	pprint(get_sqlite_files(path))
	print()
	pprint(get_tablenames(path+'permissions.sqlite'))
	pprint(get_tablenames(path+'places.sqlite'))
	pprint(get_tablenames(path+'favicons.sqlite'))
	print()
	pprint(get_fieldnames(path+'places.sqlite', 'moz_places'))
	pprint(get_fieldnames(path+'places.sqlite','moz_bookmarks'))
	pprint(get_fieldnames(path + 'favicons.sqlite', 'moz_icons'))
	print()


def recon_chrome():
	path = 'C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\history\\'
	pprint(get_tablenames(path))
	pprint(get_fieldnames(path, 'urls'))
	pprint(get_fieldnames(path, 'meta'))

if __name__ == '__main__':
	recon_firefox()
	recon_chrome()


