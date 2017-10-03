from array import array
from bisect import insort

import db_handler
import show
import helpers


def merge_databases(source_record_yielder, sink_db_info, start_from=0, print_records=False):
	each_time = int(print_records)
	url_hashes = array('Q')
	for count, record in enumerate(source_record_yielder):
		if count < start_from and start_from:
			continue
		curr_record_hash = list(record.keys())[0]
		
		if curr_record_hash not in set(url_hashes):
			insort(url_hashes, curr_record_hash)
			try:
				field_names_string
			except NameError:
				field_names_string, data = helpers.get_record_info(record)
				queries = helpers.make_queries(table='moz_places',
				                                    field_names=field_names_string)
				helpers.create_table(cursor=sink_db_info['cursor'], query=queries['create'])
			finally:
				data = list(record[curr_record_hash].values())
				helpers.insert_record(connection=sink_db_info['connection'],
				                           cursor=sink_db_info['cursor'],
				                           query=queries['insert'],
				                           data=data)
			
			show.show_record_(record=record, record_count=count, each_time=each_time)
	return url_hashes


def write_to_db(database, record, table='moz_places'):
	
	field_names_string, data = helpers.get_record_info(record)
	# table_name = ['moz_places']
	queries = helpers.make_queries(table, field_names_string)
	conn, cur, filepath = db_handler.connect_db(database)
	
	helpers.create_table(cursor=cur, query=queries['create'])
	helpers.insert_record(connection=conn, cursor=cur, query=queries['insert'], data=data)
	
	conn.close()
	
	

def write_to_json(json_path, record_yielder):
	import jsonlines
	
	with jsonlines.open(json_path, 'w') as json_records_obj:
		for record in record_yielder:
			json_records_obj.write(record)





if __name__ == '__main__':
	pass
