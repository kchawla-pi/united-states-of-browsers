import sqlite3

from tests.table import test_table_setup as tts
from united_states_of_browsers.db_merge.table import Table


browser_info = tuple(tts.no_error_test_setup())
sort_fn = lambda item: item['url']
fields_to_compare = ('url', 'title', 'last_visit')

for browser_ in browser_info:
	table_obj = Table(*browser_)
	table_obj.get_records()
	
	with sqlite3.connect(str(browser_.path)) as conn:
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()
		query_result = cur.execute(f'SELECT * FROM {browser_.table}')
		direct_connect_records_yielder = (dict(result) for result in query_result)
	
	table_obj_records = sorted(list(table_obj.records_yielder), key=sort_fn)
	direct_connect_records = sorted(list(direct_connect_records_yielder), key=sort_fn)
	
	for table_record, direct_record in zip(table_obj_records, direct_connect_records):
		assert table_record['url'] == direct_record['url']
		assert table_record['title'] == direct_record['title']
		assert (
				table_record.get('last_visit_time', table_record.get('last_visit_date'))
				==
				direct_record.get('last_visit_time', direct_record.get('last_visit_date'))
		)
