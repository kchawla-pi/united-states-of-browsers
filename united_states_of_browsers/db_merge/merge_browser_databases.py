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

from united_states_of_browsers.db_merge import (database_operations as db_ops,
                                                db_search,
                                                )
from united_states_of_browsers.db_merge.paths_setup import app_inf_path
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
	app_inf = db_ops.make_database_filepaths(output_db=output_db, profiles=profiles)
	
	source_records_yielder = db_ops.yield_source_records(source_db_paths=app_inf['source'],
	                                              source_fieldnames=app_inf['source_fieldnames'])
	if app_inf['sink']:
		db_ops.write_new_database(sink_db_path=app_inf['sink'],
		                   table=table,
		                   fieldnames=app_inf['source_fieldnames'],
		                   source_records=source_records_yielder
		                   )
		with open(app_inf_path, 'w') as json_obj:
			json.dump(app_inf, json_obj, indent=4, ensure_ascii=False)
			
		db_search.build_search_table(db_path=app_inf['sink'], included_fieldnames=app_inf['search_fieldnames'])
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
		            'Press <n> to abort, <ENTER> for viewing the merged results without writing it to a new database file.\n'
		            'Type a filename to write the merged results to a database file.')
		if ask.lower() == 'n':
			print('Program terminated.')
			os.sys.exit()
		elif not ask:
			merged_records = (tuple(merge_records(output_db=None, profiles=None, table='moz_places')))
			show = input('Records merged. If you would like to see them, press ENTER now, else press <n> key')
			if show == 'n'.lower():
				pass
			else:
				pprint(merged_records)
		elif ask:
			merge_records(output_db=f'{ask}.sqlite', profiles=None, table='moz_places')
	
	
	_main()
