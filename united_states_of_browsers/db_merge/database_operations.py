# -*- encoding: utf-8 -*-
"""
Contains functions for reading from, creating, and writing to, databases.

Avaliable functions:
 - make_database_filepaths: Returns a dict of filepaths to read from and write to.
 - yield_source_records: Uses database filepaths to yield namedtuples of records.
 - write_new_write_new_database: Creates or/and populates a database.
"""
import sqlite3
from collections import namedtuple, OrderedDict as odict
from datetime import datetime as dt

from united_states_of_browsers.db_merge import (browser_specific_setup,
                                                helpers,
                                                paths_setup
                                                )
from united_states_of_browsers.db_merge.imported_annotations import *


DBRecord = []


def make_database_filepaths(output_db: Union[None, Text],
                            profiles: Optional[Union[Text, Iterable[Text]]]=None
                            ) -> Dict[Text, PathInfo]:
	""" Returns dict of path of files.
	Accepts output database name and browser profiles.
	
	output_db: Union[filename.fileext, filename, None]. If None, records are not written to database file.
	profiles: Union[browser profile, list of browser profiles, None]. If None, includes all profiles.
	
	returns:
		{
		'source': Databases to read from {profile name: profile paths},
		'sink': database to write to,
		'hash': filepath to hashes of urls written,
		'source_fieldnames': list of fieldnames in source databases
		}
	"""
	source_db_paths, source_fieldnames, source_search_fields = browser_specific_setup.firefox(profiles=profiles)
	appdata_path, sink_db_path, url_hash_log_file = paths_setup.setup_output_db_paths(output_db)
	file_paths = {'source': source_db_paths,
	              'source_fieldnames': [*source_fieldnames, 'last_visit_date_readable'],
	              'search_fieldnames': source_search_fields,
	              'sink': sink_db_path,
	              'hash': url_hash_log_file,
	              'appdata_path': str(appdata_path),
	              }
	return file_paths  # collected in a dict, to be written to a JSON file.


def yield_source_records(source_db_paths: Dict[Text, PathInfo],
                         source_fieldnames: Sequence[Text]
                         ) -> Generator[NamedTuple, None, None]:
	""" Returns a generator of named tuple which can yield a record across all database files.
	Accepts dict of profile names and their database filepaths; and inclusive list of fieldnames.
	
	source_db_paths: {Profile names: profile database filepaths}
	source_fieldnames: list of fieldnames inclusive of all the fieldnames across all database files.
	
	returns: Generator of namedtuple which can yield each record.
	"""
	global DBRecord
	# Additional field to store last_visited_date field value converted from microsceonds to human usable format.
	# source_fieldnames.append('visited_on')  # will likely be moved to browser specific settings, when otjer browsers are added.
	DBRecord = namedtuple('DBRecord', source_fieldnames)
	incr = helpers.incrementer()
	source_records_template = odict.fromkeys(source_fieldnames, None)
	for profile_name, profile_db_path in source_db_paths.items():
		with sqlite3.connect(profile_db_path) as source_conn:
			source_conn.row_factory = sqlite3.Row
			try:
				for db_record_yielder in source_conn.execute("""SELECT * FROM moz_places WHERE title IS NOT NULL"""):
					''' Prevents adding additional keys, only updates keys/fields specified in source_fieldnames.
					Prevents field mismatches among profiles, ex: favicon_url in Firefox exists in some profiles not in others.
					'''
					source_records_template = odict(
								(key, dict(db_record_yielder).setdefault(key, None))
									for key in source_records_template)
					# Couldn't figure out how to make AUTOINCREMENT PRIMARY KEY work in SQL, hence this serial# generator.
					source_records_template['id'] = next(incr)
					try:
						source_records_template['last_visit_date_readable'] = dt.fromtimestamp(source_records_template['last_visit_date'] // 10**6).strftime('%c')
					except TypeError:
						pass
					# OrderedDict converted to NamedTuple as tuples easily convert to SQL query bindings.
					yield DBRecord(*source_records_template.values())
			except sqlite3.OperationalError:
				print(f'This browser profile does not seem to have any data: {profile_name}')


def write_new_database(sink_db_path: PathInfo,
                       fieldnames: Sequence[Text],
                       source_records: Iterable[Sequence[Text]],
                       table: Text='moz_places'
                       ) -> None:
	""" Creates or/and populates a database.
	Accepts path of destination database file, list of fieldnames for each record,
	a record yielding generator.
		Optionally can accept a table name.
	
	sink_db_path: Path to the output database file.
		If None, returns the merged records instead of writing them.
	fieldnames: List of fieldnames for the output database.
		Typically autogenerated from source database.
	source_records: Generator which yields the records to be merged.
	table: name of table in the database. Default is 'moz_places'.
	"""
	sink_fieldnames = fieldnames[:]  # create a copy of fieldnames values.
	table = helpers.query_sanitizer(table)
	sink_fieldnames = [helpers.query_sanitizer(fieldname_) for fieldname_ in sink_fieldnames]
	
	with sqlite3.connect(sink_db_path) as sink_conn:
		sink_queries = helpers.make_queries(table=table, fieldnames=sink_fieldnames)
		try:
			sink_conn.executemany(sink_queries['insert'], source_records)
		except Exception as excep:
			table_exists_text = f'table {table} already exists'
			''' Workaround for more granular exception handling. 
			Addresses SQLite3's broad exceptions, in-lieu of custom exception classes.
			'''
			if 'UNIQUE constraint failed:' in str(excep):
				raise (excep)
			elif table_exists_text in str(excep):
				print(f'{table_exists_text}.')
			elif f'no such table: {table}' in str(excep):
				sink_conn.execute(sink_queries['create'])
				sink_conn.executemany(sink_queries['insert'], source_records)
			else:
				print('Unanticipated exception:')
				raise (excep)
