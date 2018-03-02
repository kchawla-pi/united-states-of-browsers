import sqlite3

from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge.orchestrator import Orchestrator
from united_states_of_browsers.db_merge.browser_data import prep_browsers_info

app_path = '~/USB/for_tests'
db_name = 'merged_db_for_testing.sqlite'

read_from_path_prefix = Path(__file__).parents[1].joinpath('tests', 'data', 'browser_profiles_for_testing')
compare_with_db_path = Path(__file__).parents[1].joinpath('tests', 'data', '~benchmark_merged_browser_db.sqlite')

browser_info = prep_browsers_info(parent_dir=read_from_path_prefix)
test_orchestrator = Orchestrator(app_path=app_path, db_name=db_name, browser_info=browser_info)
test_orchestrator.orchestrate()

newly_merged_test_db_path = Path(app_path, db_name).expanduser()

print(newly_merged_test_db_path, compare_with_db_path, sep='\n')
with sqlite3.connect(str(newly_merged_test_db_path)) as new_db_conn:
	new_db_conn.row_factory = sqlite3.Row
	new_db_cur = new_db_conn.cursor()
	new_db_query_result = new_db_cur.execute('SELECT * FROM history')

with sqlite3.connect(str(compare_with_db_path)) as benchmark_db_conn:
	benchmark_db_conn.row_factory = sqlite3.Row
	benchmark_db_cur = benchmark_db_conn.cursor()
	benchmark_db_query_result = benchmark_db_cur.execute('SELECT * FROM history')

sort_fn = lambda item: item['url']
new_db_records = sorted([dict(record) for record in new_db_query_result], key=sort_fn)
benchmark_db_records = sorted([dict(record) for record in benchmark_db_query_result], key=sort_fn)

comparision_results = all([bench_record[bench_key] == new_record[bench_key]
                           for bench_record, new_record in zip(benchmark_db_records, new_db_records)
                           for bench_key in bench_record
                           ])
if not comparision_results:
	for bench_record, new_record in zip(benchmark_db_records, new_db_records):
		for bench_key in bench_record:
			if bench_key not in ('last_visit', 'title'):
				# if bench_key['title']
				if bench_record[bench_key] != new_record[bench_key]:
					pprint((bench_key, bench_record[bench_key], new_record[bench_key]))
				
print(comparision_results)

print()
