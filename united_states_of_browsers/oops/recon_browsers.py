import sqlite3

from pprint import pprint


def print_objects(objects_list):
	for obj in objects_list:
		print('repr:', repr(obj))
		pprint(obj)
		print('-' * 25)

def get_tablenames(path):
	with sqlite3.connect(str(path)) as conn:
		cur = conn.cursor()
		query = 'SELECT name FROM sqlite_master where type == "table"'
		query_result = cur.execute(query)
		pprint([result[0] for result in query_result])

def print_tables(table_yielders):
	for tablename, table in table_yielders.items():
		try:
			print(tablename, ':', list(dict(table.records_yielder.fetchone()).keys()))
			# for record in table.records_yielder:
			# 	print(dict(record), '\n')
		except (TypeError, AttributeError) as excep:
			pass
			# print('No records retrieved.')

if __name__ == '__main__':
	print(get_tablenames('C:/Users/kshit/AppData/Roaming/Mozilla/Firefox/Profiles/e0pj4lec.test_profile0/permissions.sqlite'))
