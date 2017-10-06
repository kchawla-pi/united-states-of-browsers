# -*- encoding: utf-8 -*-
from array import array
from bisect import insort
from collections import OrderedDict as odict

import show
from annotations import *

from db_merge import helpers


def merge_databases(source_record_yielder: Generator,
                    sink_db_info: Dict,
                    start_from: int=0,
                    print_records: Union[bool, int]=False
                    ) -> Sequence[int]:
	'''
	Creates a new database by merging data from multiple databases.
	Accepts a generator to yield source databases records, dict of info for target database.
	Optional: Accepts the number of initial records to skip, and to print the records as they are processed.
	Returns array of url_hashes of website addresses.
	'''
	each_time = int(print_records)
	url_hashes = array('Q')
	for count, record in enumerate(source_record_yielder):
		if count < start_from and start_from:
			continue
		curr_record_hash = list(record.keys())[0]
		
		if curr_record_hash not in set(url_hashes):
			written_url_hash = write_to_db(record=record, sink_db_info=sink_db_info, table='moz_places')
			insort(url_hashes, written_url_hash)
			
			show.show_record_(record=record, record_count=count, each_time=each_time)
	return url_hashes


def write_to_db(record: Dict, sink_db_info: Dict, table: Text='moz_places') -> int:
	'''
	Writes a record to a database.
	Accepts a record and target database info
	Optional: database table name else uses default 'moz_places'.
	Returns the url_hash of the written record.'''
	curr_record_hash = list(record.keys())[0]
	try:
		field_names_string
	except NameError:
		field_names_string, data = helpers.get_record_info(record)
		queries = helpers.make_queries(table=table, field_names=field_names_string)
		helpers.create_table(cursor=sink_db_info['cursor'], query=queries['create'])
	
	data = list(record[curr_record_hash].values())
	try:
		helpers.insert_record(connection=sink_db_info['connection'], cursor=sink_db_info['cursor'],
		                      query=queries['insert'], data=data)
	except Exception as excep:
		raise excep
	else:
		return curr_record_hash
		
	
	

def write_to_json(json_path, record_yielder):
	'''Deprecated'''
	import jsonlines
	
	with jsonlines.open(json_path, 'w') as json_records_obj:
		for record in record_yielder:
			json_records_obj.write(record)





if __name__ == '__main__':
	test_records = (
		{47356370932282: odict(
				[('id', 1), ('url', 'https://www.mozilla.org/en-US/firefox/central/'),
				 ('title', None), ('rev_host', 'gro.allizom.www.'), ('visit_count', 0),
				 ('hidden', 0), ('typed', 0), ('favicon_id', None), ('frecency', 74),
				 ('last_visit_date', None), ('guid', 'NNqZA_f2KHI1'), ('foreign_count', 1),
				 ('url_hash', 47356370932282), ('description', None), ('preview_image_url', None)])},
		{47357795150914: dict(odict(
				[('id', 2), ('url', 'https://support.mozilla.org/en-US/products/firefox'),
				 ('title', None), ('rev_host', 'gro.allizom.troppus.'), ('visit_count', 0),
				 ('hidden', 0), ('typed', 0), ('favicon_id', None), ('frecency', 74),
				 ('last_visit_date', None), ('guid', '4xhwpotXndUs'), ('foreign_count', 1),
				 ('url_hash', 47357795150914), ('description', None), ('preview_image_url', None)]))},
		)
	import jsonlines
	# for record in test_records:
		# write_to_json('example_json.jsonl', record)
	with jsonlines.open('example_json.jsonl', 'w') as json_records_obj:
		for record in test_records:
			json_records_obj.write(record)
