def test_firefox():
	profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	firefox = Browser('firefox', profile_pathcrumbs_firefox, ['places.sqlite', 'favicons.sqlite', 'arbit'])
	firefox.setup_paths()
	print((firefox.db_info[0])['path'])

	one_file = DBFile((firefox.db_info[0])['path'])
	one_file._connect()
	one_file._tables_info()
	# print(one_file.tablenames)


	# Table((one_file.tablenames[0])

	one_file.read_tables()
	# pprint(one_file.tables)
	# print(one_file.tables[0])
	# print([dict(record) for record in one_file.tables[0].record_yielder])

def test_Table(path):
	with sqlite3.connect(path) as connection:
		table = Table('moz_places', connection)
		print(table)

def other():
	profile_pathcrumbs_firefox = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
	chrome_path = f'~\\AppData\\Local\\Google\\Chrome\\User Data'

	firefox = Browser('firefox', profile_pathcrumbs_firefox, ['places.sqlite', 'favicons.sqlite', 'arbit'])
	firefox.setup_paths()

	print((firefox.db_info[0])['path'])
	one_file = DBFile((firefox.db_info[0])['path'])
	one_file._connect()
	one_file._tables_info()
	pprint(one_file.tablenames)
	# pprint(one_file.tables_info)
	# pprint(one_file._tables_fields())

	# one_profile_cur = one_file._connect()
	# query_result = one_profile_cur.execute('SELECT * FROM sqlite_master')
	# query_ans = [dict(entry) for entry in query_result]
	# print(query_ans)
	# pprint(firefox.db_info)


	# firefox.read_table_info()
	# chrome = Browser('chrome', [chrome_path], ['history_copy'])
	# print(chrome)
	# chrome.setup_paths()
	# chrome.read_table_info()
	# pprint(chrome['db_info'])

	# print(firefox['browser'])
	# print(firefox['pathcrumbs'])
	# print(firefox['browser'])
	# print(firefox.__dict__.keys())

	# temp_path = db_paths[('test_profile0', 'arbit')]; temp_conn = f'file:{temp_path}?mode=ro'; temp_gen = self._connect(temp_path); print(next(temp_gen, None))
if __name__ == '__main__':
	test_firefox()


"""
Separate connect out as a separate function.
"""
