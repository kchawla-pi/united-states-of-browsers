import shutil
import sqlite3

from pathlib import Path
from pprint import pprint


def groupby(db_path):
	with sqlite3.connect(str(db_path)) as conn:
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()
		# cur.
		# query = f'SELECT {fieldnames_str} FROM {table} GROUP BY {grouping_field} ORDER BY {ordering_field}'
		# query = f'SELECT * FROM history'
		query = f'SELECT * FROM history WHERE title LIKE "rwby%" GROUP BY title'
		query_result = cur.execute(query)
		# result = query_result.fetchmany(150)
		result = [dict(record) for record in query_result]
		result_dups_url_specific = [record for record in result if record['url']=='https://www.google.com/search?q=rwby+volume+5+chapter+8&ie=utf-8&oe=utf-8&client=firefox-b-1-ab']
		result_dups_urls = [record['url'] for record in result]
		result_dups_titles = [record['title'] for record in result]
		pprint(result)
		# print(len(result), len(set(result)))
		# pprint(result_dups_urls)
		print('title', len(result_dups_titles), len(set(result_dups_titles)))
		print('url', len(result_dups_urls), len(set(result_dups_urls)))


def copy_db(src_db, dst_db):
	shutil.copy2(src_db, dst_db)


if __name__ == '__main__':
	db_path = Path(r"C:\Users\kshit\OneDrive\workspace\UnitedStatesOfBrowsers\united_states_of_browsers\oops\combined_db_fx_cr.sqlite")
	table = 'history'
	fieldnames = ['id', 'url', 'title', 'last_visit_date']
	grouping_field = 'url'
	ordering_field = 'last_visit_date'
	fieldnames_str = ', '.join(fieldnames)
	src_db = Path(r"C:\Users\kshit\AppData\Local\Google\Chrome\User Data\Default\History")
	dst_db = Path(r"C:\Users\kshit\OneDrive\workspace\UnitedStatesOfBrowsers\united_states_of_browsers\oops")
	copy_db(src_db, dst_db)
