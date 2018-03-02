# -*- encoding: utf-8 -*-
"""
Ad-hoc, non production code for comparing search results yielded via fts5 and python's 'in' keyword.
"""
import sqlite3

from collections import OrderedDict as odict
from pathlib import Path
from pprint import pprint

from tests.data.creating_test_search_data import (setup_paths as test_db_paths,
                                                  retrieve_record_using_id,
                                                  )

from united_states_of_browsers.db_merge.db_search import search as search_using_fts5


def search_using_in(db_path, query):

	with sqlite3.connect(db_path) as conn:
		conn.row_factory = sqlite3.Row
		query_result = conn.execute('''SELECT * FROM moz_places''')
	search_results = []
	for record_dict in query_result:
		for field in ['url', 'title', 'description']:
			if record_dict[field]:
				if query in record_dict[field]:
					search_results.append(odict(record_dict))
	return search_results


def print_search_results(active, from_in, from_fts):
	if not active:
		return
	pprint(from_in)
	print()
	pprint(from_fts)
	print()


def search_results_infos(db_path, query):
	results_from_search_using_in = search_using_in(db_path, query)
	results_from_search_using_fts5 = search_using_fts5(db_path=db_path, word_query=query)
	
	id_from_search_using_in = sorted([record['id'] for record in results_from_search_using_in])
	id_from_search_using_fts5 = sorted([record.id for record in results_from_search_using_fts5])
	
	in_only_id = set(id_from_search_using_in).difference(id_from_search_using_fts5)
	fts_only_id = set(id_from_search_using_fts5).difference(id_from_search_using_in)
	
	return (results_from_search_using_in, results_from_search_using_fts5,
	        id_from_search_using_in, id_from_search_using_fts5,
	        in_only_id, fts_only_id
	        )


def print_results_infos(active,results_from_search_using_in, results_from_search_using_fts5,
                        id_from_search_using_in, id_from_search_using_fts5,
                        in_only_id, fts_only_id
                        ):
	if not active:
		return
	print(f'results: in == fts5: {results_from_search_using_in == results_from_search_using_fts5}',
	      f'id_list: in == fts5: {id_from_search_using_in == id_from_search_using_fts5}',
	      f'\nid_list:',
	      f'\tin: {id_from_search_using_in}',
	      f'\tfts5:{id_from_search_using_fts5}',
	      f'\nid_exclusive_to:',
	      f'\tin: {in_only_id}',
	      f'\tfts5: {fts_only_id}',
	      sep='\n', end='\n\n'
	      )
	
def get_show_diff_info(active, show, in_only_id, fts_only_id):
	if not active:
		return
	id_lists = (in_only_id, fts_only_id)
	empty_rec_db = []
	nonempty_rec_db = []
	if show: print('id_lists')
	for id_list in id_lists:
		empty_records = []
		not_empty_records = []
		if show: print(id_list)
		for id in id_list:
			try:
				record = retrieve_record_using_id(id)[0]
			except IndexError as excep:
				empty_records.append(id)
			else:
				not_empty_records.append(id)
				if show: print(id, record['url'], record['title'], 'desc:', record['description'])
		empty_rec_db.append(empty_records)
		nonempty_rec_db.append(not_empty_records)
		if show: print()
	return id_lists, empty_rec_db, nonempty_rec_db

def show_total_is_omniset(active, id_lists, empty_rec_db, nonempty_rec_db):
	if not active:
		return
	for id_list, empty_records, not_empty_records in zip(id_lists, empty_rec_db, nonempty_rec_db):
		print('Total == empty + not empty? ', set(id_list) == set(empty_records).union((not_empty_records)))
	print('empty_rec_db[0] == empty_rec_db[1]:', empty_rec_db[0] == empty_rec_db[1])
	print('nonempty_rec_db[0] == nonempty_rec_db[1]:', nonempty_rec_db[0] == nonempty_rec_db[1])
	# print('empty_rec_db', empty_rec_db)
	print('nonempty_rec_db', nonempty_rec_db)
	
	
def setup_paths():
	root = Path(__file__).parents[1]
	db_for_testing = str(root.joinpath('tests\\data\\db_for_testing_search.sqlite'))
	db_main = str(root.joinpath('united_states_of_browsers\\db_merge\\all_merged.sqlite'))
	return {'db_for_testing': db_for_testing , 'db_main': db_main }
	
def run_comparision(query, current_db):
	(results_from_search_using_in, results_from_search_using_fts5,
	 id_from_search_using_in, id_from_search_using_fts5,
	 in_only_id, fts_only_id
	 ) = search_results_infos(db_path=current_db, query=query)
	
	print_search_results(False, results_from_search_using_in, results_from_search_using_fts5)
	print_results_infos(False, results_from_search_using_in, results_from_search_using_fts5,
	                    id_from_search_using_in, id_from_search_using_fts5,
	                    in_only_id, fts_only_id
	                    )
	
	id_lists, empty_rec_db, nonempty_rec_db = get_show_diff_info(1, 0, in_only_id, fts_only_id)
	
	show_total_is_omniset(0, id_lists, empty_rec_db, nonempty_rec_db)
	
	get_show_diff_info(1, 1, nonempty_rec_db[0], nonempty_rec_db[1])
	# pprint(nonempty_rec_db)


if __name__ == '__main__':
	queries = ['python', 'python', '"python" *']
	db_paths = setup_paths()
	
	current_db = db_paths['db_main']
	# current_db = db_paths['db_for_testing']
	print(current_db)
	for query in queries[-1]:
		print('-'*25, query, '.'*25, sep='\n', end='\n')
		run_comparision(query, current_db)
		print('.' * 25, query, '-' * 25, sep='\n', end='\n')
	
	# search_results = [record_dict['id']
	#                   for record_dict in query_result
	#                   if query in record_dict['title']
	#                   or query in record_dict['url']
	#                   or query in record_dict['description']
	#                   ]
