import sqlite3
import stat

from pathlib import Path
from pprint import pprint


def get_test_databases_info(common_path_of_all_source_db):
	return [
		(common_path_of_all_source_db.joinpath('Roaming/Mozilla/Firefox/Profiles/e0pj4lec.test_profile0', 'places.sqlite'),
		 ('firefox', 'test_profile0', 'places.sqlite'),
		 ('moz_places',),
		 ),
		
		(common_path_of_all_source_db.joinpath('Roaming/Mozilla/Firefox/Profiles/kceyj748.test_profile1', 'places.sqlite'),
		 ('firefox', 'test_profile1', 'places.sqlite'),
		 ('moz_places',),
		 ),
		
		# (path_prefix.joinpath('Roaming/Mozilla/Firefox/Profiles/udd5sttq.test_profile2', 'places.sqlite'),
		# ('firefox', 'test_profile2', 'places.sqlite'),
		# ('moz_places',),
		#  ),
		
		(common_path_of_all_source_db.joinpath('Local/Google/Chrome/User Data/Profile 1', 'history'),
		 ('chrome', 'Profile 1', 'history'),
		 ('urls',),
		 ),
		
		(common_path_of_all_source_db.joinpath('Local/Vivaldi/User Data/Default', 'History'),
		 ('vivaldi', 'Default', 'History'),
		 ('urls',),
		 ),
		
		# (path_prefix.joinpath('Opera Software/Opera Stable', 'History'),
		# ('opera', 'Opera Stable', 'History'),
		#  ('urls',),
		#  ),
		]


def get_data_yielder(browser_db_info, fields_accessed):
	query = lambda table: f'SELECT * FROM {table}'
	for db_path_, (browser, profile, file), tables in browser_db_info:
		with sqlite3.connect(str(db_path_)) as conn:
			conn.row_factory = sqlite3.Row
			cur = conn.cursor()
			for table_ in tables:
				query_result = cur.execute(query(table_))
				for row in query_result:
					selected_fields = {fieldname: data for fieldname, data in dict(row).items() if
					                   fieldname in fields_accessed}
					try:
						last_visit_data, last_visit_fieldname = selected_fields['last_visit_date'], 'last_visit_date'
					except KeyError:
						last_visit_data, last_visit_fieldname = selected_fields['last_visit_time'], 'last_visit_time'
					
					if last_visit_data:
						selected_fields.pop(last_visit_fieldname)
						selected_fields.update(last_visit_fieldname=last_visit_data)
						
						updated_row = {
							**selected_fields, 'browser': browser, 'profile': profile, 'file': file, 'tablename': table_}
						# if updated_row['l
						yield tuple(updated_row.values())


def write_data_to_db(dst_db_path, tablename, fieldnames, data_source):
	fieldnames_str = ', '.join(fieldnames)
	with sqlite3.connect(str(dst_db_path)) as conn:
		cur = conn.cursor()
		query_placeholder = '?, ' * len(fieldnames)
		cur.execute(f'CREATE TABLE IF NOT EXISTS {tablename} ({fieldnames_str})')
		# row_data = (row[fieldname_] for row in data_source for fieldname_ in fieldnames)
		cur.executemany(f'INSERT INTO {tablename} ({fieldnames_str}) VALUES ({query_placeholder[:-2]})', data_source)
		

def make_benchmark_db(common_path_of_all_source_db, dst_db_path, fields_accessed, fields_to_be_written):
	browser_db_info = get_test_databases_info(common_path_of_all_source_db=common_path_of_all_source_db)
	row_yielder = get_data_yielder(browser_db_info, fields_accessed)
	
	# all_fieldnames = (*fields_accessed, *fields_added)
	write_data_to_db(dst_db_path=dst_db_path, tablename='history', fieldnames=fields_to_be_written, data_source=row_yielder)


def make_test_data_paths(benchmark_db_name):
	path_to_project_root = Path(__file__).parents[3]  #'C:/Users/kshit/OneDrive/workspace'
	path_in_project_dir_to_test_profiles = 'UnitedStatesOfBrowsers/tests/data/browser_profiles_for_testing/AppData'
	path_in_project_to_benchmark_db = 'UnitedStatesOfBrowsers/tests/data'
	
	common_path_of_all_test_db_to_be_combined_to_make_benchmark_db = Path(path_to_project_root, path_in_project_dir_to_test_profiles)
	benchmark_db_path = Path(
			path_to_project_root,
			path_in_project_to_benchmark_db,
			benchmark_db_name,
			)
	return common_path_of_all_test_db_to_be_combined_to_make_benchmark_db, benchmark_db_path


def get_database_fieldnames():
	common_fields = ('url', 'title')
	fields_accessed = (*common_fields, 'last_visit_date', 'last_visit_time')
	fields_added = ('browser', 'profile', 'file', 'tablename')
	fields_to_be_written = (*common_fields, 'last_visit', *fields_added)
	return fields_accessed, fields_added, fields_to_be_written
	
	
def create_testing_data(benchmark_db_name):
	common_path_of_all_test_db_to_be_combined_to_make_benchmark_db, benchmark_db_path = make_test_data_paths(benchmark_db_name=benchmark_db_name)
	fields_accessed, fields_added, fields_to_be_written = get_database_fieldnames()
	
	if benchmark_db_path.exists():
		raise FileExistsError
	else:
		make_benchmark_db(
				common_path_of_all_test_db_to_be_combined_to_make_benchmark_db,
				benchmark_db_path,
				fields_accessed,
				fields_to_be_written,
				)
		benchmark_db_path.chmod(stat.S_IREAD)


if __name__ == '__main__':
	create_testing_data(benchmark_db_name='~benchmark_db_for_usb_testing.sqlite')
