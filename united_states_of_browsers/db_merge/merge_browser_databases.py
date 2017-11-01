# -*- encoding: utf-8 -*-
"""
Contains functions to merge the records from multiple Firefox profiles.

Available functions:
 - merge_records: Accepts output database name, list of browser profiles, database table name.
        Returns Tuple of records, or writes them to disk.
"""
import json
import os
from pprint import pprint

from united_states_of_browsers.db_merge import database_operations as db_ops
from united_states_of_browsers.db_merge.imported_annotations import *


def merge_records(output_db: Union[Text, None],
                  profiles: Union[Text, Iterable[Text], None],
                  table: Text
                  ) -> Union[None, Generator[Sequence[NamedTuple], None, None]]:
	""" Returns Tuple of records or writes them to disk.
	Accepts output database name, list of browser profiles, and database table name.
	
	output_db: Name of database file to write to.
		If None, returns the records without writing to disk.
	profiles: Name of a single profile or list of profiles to read from.
		If None, reads from all the profiles found.
	table: Name of table in database file to read from. Default is 'moz_places'.
	
	returns: Returns None if database is written to disk. Returns tuple of records otherwise.
	"""
	file_paths = db_ops.make_database_filepaths(output_db=output_db, profiles=profiles)
	
	source_records_yielder = db_ops.yield_source_records(source_db_paths=file_paths['source'],
	                                              source_fieldnames=file_paths['source_fields'])
	if file_paths['sink']:
		db_ops.write_new_database(sink_db_path=file_paths['sink'],
		                   table=table,
		                   fieldnames=file_paths['source_fields'],
		                   source_records=source_records_yielder
		                   )
		with open('path_info.json', 'w') as json_obj:
			json.dump(file_paths, json_obj, indent=4, ensure_ascii=False)
		included_fieldnames = ('url', 'title', 'visit_count', 'last_visit_date', 'url_hash', 'description')
		# db_search.build_search_table(path_info=file_paths, included_fieldnames=included_fieldnames)
	else:
		# return {record.url_hash: record._asdict() for record in source_records_yielder}
		return source_records_yielder
		

if __name__ == '__main__':
	def _test():
		profiles = None
		output_db = 'test_new_allmerged.sqlite'
		table = 'moz_places'
		merge_records(output_db=output_db, profiles=profiles, table=table)
		pprint(merge_records(output_db=None, profiles=profiles, table=table))
		
		profiles = ['dev-edition-default', 'test_profile0', 'test_profile1']
		output_db = 'test_new_01_dev.sqlite'
		merge_records(output_db=output_db, profiles=profiles, table=table)
		pprint(tuple(merge_records(output_db=None, profiles=profiles, table=table)))
		
		
	def _main():
		ask = input('Run database merge_records operation?\n'
		            'Press <n> to abort, <ENTER> for viewing the merged reuslts without writing it to a new database file.\n'
		            'Type a filename to write the merged results to a database file.')
		if ask.lower() == 'n':
			print('Program terminated.')
			os.sys.exit()
		elif not ask:
			pprint(tuple(merge_records(output_db=None, profiles=None, table='moz_places')))
		elif ask:
			merge_records(output_db=f'{ask}.sqlite', profiles=None, table='moz_places')
	
	
	_main()
