import sqlite3

from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge.db_merge import DatabaseMergeOrchestrator
from united_states_of_browsers.db_merge.browser_data import prep_browsers_info
from tests.integration_test import create_benchmark_database_for_tests


def make_test_db_path(app_path, newly_merged_test_db_name, benchmark_db_name):
	newly_merged_test_db_path = Path(app_path, newly_merged_test_db_name).expanduser()
	common_path_of_source_test_databases = Path(__file__).parents[1].joinpath('data', 'browser_profiles_for_testing')
	benchmark_db_path = Path(__file__).parents[1].joinpath('data', benchmark_db_name)
	return (
		common_path_of_source_test_databases,
		newly_merged_test_db_path,
		benchmark_db_path,
		)


def make_record_yielders_for_newly_merged_db_and_benchmark_db(newly_merged_test_db_path, benchmark_db_path):
	with sqlite3.connect(f'{newly_merged_test_db_path}') as new_db_connection:
		new_db_connection.row_factory = sqlite3.Row
		new_db_cur = new_db_connection.cursor()
		new_db_query_record_yielder = new_db_cur.execute('SELECT * FROM history')
	
	with sqlite3.connect(f'{benchmark_db_path}') as benchmark_db_connection:
		benchmark_db_connection.row_factory = sqlite3.Row
		benchmark_db_cur = benchmark_db_connection.cursor()
		benchmark_db_query_record_yielder = benchmark_db_cur.execute('SELECT * FROM history')
	
	return new_db_query_record_yielder, benchmark_db_query_record_yielder


def get_sorted_records_from_record_yielders(new_db_record_yielder, benchmark_db_record_yielder):
	sort_fn = lambda item: item['url']
	first_db_records = sorted([dict(record) for record in new_db_record_yielder], key=sort_fn)
	second_db_records = sorted([dict(record) for record in benchmark_db_record_yielder], key=sort_fn)
	return first_db_records, second_db_records


def make_finer_grained_db_comparision_assertions(benchmark_db_records, new_db_records):
	assert len(benchmark_db_records) == len(new_db_records), (len(benchmark_db_records), '**', len(new_db_records))
	
	benchmark_db_records_keys = set(
			[tuple(benchmark_db_record_.keys()) for benchmark_db_record_ in benchmark_db_records])
	assert len(benchmark_db_records_keys) == 1, len(benchmark_db_records_keys)
	
	new_db_records_keys = set([tuple(new_db_record_.keys()) for new_db_record_ in new_db_records])
	assert len(new_db_records_keys) == 1, len(new_db_records_keys)
	
	benchmark_db_records_keys = set(*benchmark_db_records_keys)
	new_db_records_keys = set(*new_db_records_keys)
	assert benchmark_db_records_keys.issubset(new_db_records_keys), benchmark_db_records_keys.difference(
		new_db_records_keys)
	
	_, fields_added, _ = create_benchmark_database_for_tests.get_database_fieldnames()
	additional_fields = {'last_visit_readable', 'visit_count', 'id', 'rec_num'}
	expected_fields_in_new_merged_db = set([*benchmark_db_records_keys, *fields_added, *additional_fields])
	assert expected_fields_in_new_merged_db == new_db_records_keys, expected_fields_in_new_merged_db.symmetric_difference(
		new_db_records_keys)


def compare_new_db_and_benchmark_db(benchmark_db_records, new_db_records, newly_merged_test_db_path, benchmark_db_path):
	comparision_results = all([bench_record[bench_key] == new_record[bench_key]
	                           for bench_record, new_record in zip(benchmark_db_records, new_db_records)
	                           for bench_key in bench_record
	                           ])
	try:
		assert comparision_results
	except AssertionError:
		make_finer_grained_db_comparision_assertions(benchmark_db_records, new_db_records)
		print(f'Path of newly merged database for testing:\n\t{newly_merged_test_db_path}',
		      f'Path of benchmark database for expected result:\n\t{benchmark_db_path}',
		      sep='\n')
		non_matching_fields_yielder = yield_non_matching_fields(benchmark_db_records, new_db_records)
		return non_matching_fields_yielder
	else:
		return None


def yield_non_matching_fields(benchmark_db_records, new_db_records):
	for benchmark_db_record_, newly_created_db_record_ in zip(benchmark_db_records, new_db_records):
		for benchmark_record_fieldname in benchmark_db_record_:
			if benchmark_db_record_[benchmark_record_fieldname] == newly_created_db_record_[benchmark_record_fieldname]:
				yield (
					benchmark_record_fieldname,
					benchmark_db_record_[benchmark_record_fieldname],
					newly_created_db_record_[benchmark_record_fieldname],
					)


def test_db_merge_operation(app_path, newly_merged_test_db_name, benchmark_db_name):
	(common_path_of_source_test_databases, newly_merged_test_db_path, benchmark_db_path,
		) = make_test_db_path(app_path=app_path, newly_merged_test_db_name=newly_merged_test_db_name, benchmark_db_name=benchmark_db_name)
	
	browser_info = prep_browsers_info(parent_dir=common_path_of_source_test_databases)
	test_orchestrator = DatabaseMergeOrchestrator(app_path=app_path, db_name=newly_merged_test_db_name, browser_info=browser_info)
	test_orchestrator.orchestrate_db_merge()
	new_db_query_record_yielder, benchmark_db_query_record_yielder = make_record_yielders_for_newly_merged_db_and_benchmark_db(
			newly_merged_test_db_path,
			benchmark_db_path,
			)
	new_db_records, benchmark_db_records = get_sorted_records_from_record_yielders(
			new_db_record_yielder=new_db_query_record_yielder,
			benchmark_db_record_yielder=benchmark_db_query_record_yielder,
			)
	non_matching_fields_yielder = compare_new_db_and_benchmark_db(benchmark_db_records, new_db_records, newly_merged_test_db_path, benchmark_db_path)
	if not non_matching_fields_yielder:
		print('Passed.', '\n\n')
	else:
		pprint(list(non_matching_fields_yielder))


def db_merge_integration_test(app_path, newly_merged_db_name, benchmark_db_name):
	try:
		create_benchmark_database_for_tests.create_testing_data(benchmark_db_name='~benchmark_db_for_usb_testing.sqlite')
	except FileExistsError:
		print(f'Using existing benchmark database...')
	else:
		print(f'Test benchmark database created...')
	finally:
		print(f'Testing database merge operation.')
		test_db_merge_operation(app_path, newly_merged_test_db_name=newly_merged_db_name, benchmark_db_name=benchmark_db_name)


def run_expected_to_pass_test():
	app_path = '~/USB/for_tests'
	newly_merged_db_name = 'merged_db_for_testing.sqlite'
	benchmark_db_name = '~benchmark_db_for_usb_testing.sqlite'
	db_merge_integration_test(app_path, newly_merged_db_name, benchmark_db_name)
	

def run_expected_to_fail_test():
	app_path = '~/USB/for_tests'
	newly_merged_db_name = 'merged_db_for_testing.sqlite'
	benchmark_db_name = '~benchmark_db_for_usb_testing_deliberately_incorrect.sqlite'
	db_merge_integration_test(app_path, newly_merged_db_name, benchmark_db_name)


if __name__ == '__main__':
	run_expected_to_pass_test()
	# run_expected_to_fail_test()
