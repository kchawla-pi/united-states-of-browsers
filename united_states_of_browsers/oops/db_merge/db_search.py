import sqlite3

from datetime import datetime as dt
from pprint import pprint

from united_states_of_browsers.db_merge import helpers

from united_states_of_browsers.oops.db_merge.imported_annotations import *


def _make_sql_statement(word_query: Optional[Text],
                        date_start: Union[int, None],
                        date_stop: Union[int, None]
                        ) -> Union[Text, Iterable[Text]]:
	""" Returns prepared SQL statements and bindings for queries with and without dates.
	If no args provided, returns a search query which will select all records.
		Optional: word_query, date_start and date_stop.
	"""
	if not word_query:
		sql_query = ('SELECT * FROM search_table'
		             ' WHERE rec_id IN'
		             ' (SELECT rec_id'
		             ' FROM search_table'
		             ' WHERE last_visit BETWEEN ? AND ?)'
		             )
		query_bindings = [date_start, date_stop]
	else:
		sql_query = ('SELECT * FROM search_table'
		             ' WHERE rec_id IN'
		             ' (SELECT rec_id'
		             ' FROM search_table'
		             ' WHERE search_table'
		             ' MATCH ? ORDER BY bm25(search_table, 0, 0, 7, 9, 10, 0, 0, 0, 0)) AND last_visit BETWEEN ? AND ?'
		             )
		query_bindings = [word_query, date_start, date_stop]
	return sql_query, query_bindings


def _run_search(db_ref: PathInfo, sql_query: Text, query_bindings: Iterable[Text]
                ) -> Iterable[NamedTuple]:
	""" Returns the search results as a list of NamedTuples of records.
	Accepts --
	db_path: database file path,
	sql_query: a formed SQL query,
	query_bindings: list of attributes for the query.
	"""
	try:
		query_results = db_ref.execute(sql_query, query_bindings)
	except AttributeError:
		with sqlite3.connect(db_ref) as sink_conn:
			sink_conn.row_factory = sqlite3.Row
			query_results = sink_conn.execute(sql_query, query_bindings)
	return query_results


def _print_search(search_results: Iterable, show_only_id=False):
	formatted_results = []
	for result in search_results:
		timestamp_ = result.last_visit_date
		try:
			human_readable_date = dt.utcfromtimestamp(timestamp_ / 10 ** 6)
		except TypeError:
			human_readable_date = 'Date Unavailable'
		if show_only_id:
			result_rec = result.rec_id
		else:
			result_rec = result.title if result.title else result.url
		formatted_results.append(f'{human_readable_date}, . , {result_rec}')
		pprint(formatted_results)


def parse_and_or_not(query):
	query = query.lower()
	query = helpers.query_sanitizer(query,allowed_chars=' ')

	words = query.split()
	words_dict = {idx: word for idx, word in enumerate(words)}
	words_succeeding_term = dict.fromkeys(['or', 'not', 'and'])

	not_words_indices = [idx+1 for idx, word_ in words_dict.items() if word_ == 'not']
	words_succeeding_term['not'] = [words_dict.pop(idx) for idx in not_words_indices]
	[words_dict.pop(idx-1) for idx in not_words_indices]

	or_words_indices = [idx + 1 for idx, word_ in enumerate(words) if word_ == 'or']
	words_succeeding_term['or'] = [words_dict.pop(idx) for idx in or_words_indices]
	[words_dict.pop(idx - 1) for idx in or_words_indices]

	and_indices = [idx for idx, word_ in enumerate(words) if word_ == 'and']
	[words_dict.pop(idx) for idx in and_indices]
	words_succeeding_term['and'] = list(words_dict.values())

	return words_succeeding_term


def search(db_path: PathInfo,
           word_query: Optional[Text]='',
           date_start: Optional[Text]=None,
           date_stop: Optional[Text]=None,
           ) -> Iterable[NamedTuple]:
	""" Returns the search result as a list of NamedTuple of records.
	Accepts database file path and optionally, keywords and date range.

	Optional:
		word_query: if None (default), not included in search filter.
		date_start: if None(default), the earliest date is used.
		date_stop: if None (default), the present date is used.
	"""
	if not date_start:
		date_start = int(dt.timestamp(dt.strptime('1970-01-02', '%Y-%m-%d')) * 10**6)
	else:
		date_start = int(dt.timestamp(dt.strptime(date_start, '%Y-%m-%d')) * 10**6)
	if not date_stop:
		date_stop = int(dt.utcnow().timestamp() * 10 ** 6)
	else:
		date_stop = int(dt.timestamp(dt.strptime(date_stop, '%Y-%m-%d')) * 10**6)
	word_query = helpers.query_sanitizer(word_query, allowed_chars=[' ', '%', '(', ')', '_'])
	sql_query, query_bindings = _make_sql_statement(word_query, date_start, date_stop)
	search_results = _run_search(db_path, sql_query, query_bindings)
	return search_results


if __name__ == '__main__':
	def _test_search(db_path, show_only_id=False):
		query_dates = (1501259124168000, 1506703039399000, 1509123590555000)
		human_times = {timestamp_: dt.utcfromtimestamp(timestamp_ / 10 ** 6) for timestamp_ in
		               query_dates}

		search_test_cases = (
			(db_path, 'python~', None, None),
			(db_path, 'python', query_dates[0], None),
			(db_path, 'python', None, query_dates[0]),
			(db_path, 'python', query_dates[0], query_dates[2]),
			(db_path, [], query_dates[1], query_dates[0]),
			(db_path, "python AND variable NOT update anaconda AND stackoverflow", None, None),
			(db_path, 'india AND economy', None, None),
			(db_path, 'javascript AND economy', None, None),
			(db_path, 'javascript python NOT react', None, None),
			)

		pprint(human_times)
		for (db_path, word_query, date_start, date_stop) in search_test_cases[3:4]:
			date_start_str = f'Start Date: {date_start} -- {human_times.get(date_start, "n/a")}'
			date_stop_str = f'Start Stop: {date_stop} -- {human_times.get(date_stop, "n/a")}'
			print('-' * 25)
			print(f'word_query: {word_query},\n{date_start_str},\n{date_stop_str}')
			search_results = search(db_path, word_query, date_start, date_stop)
			_print_search(search_results, show_only_id=show_only_id)
			print()


	def test_query_validity(queries, db_test):
		for query in queries:
			helpers.query_sanitizer(query)
			try:
				search_result = search(db_test, query)
			except Exception as excep:
				print(f'Query Failed:{query}.\n Error: {excep.args}')
			else:
				print('\n', 'v' * 15, query, 'v' * 15)
				print(f'\nquery: {query}')
				pprint((search_result))
				print('^' * 15, query, '^' * 15)
		print()


	def test_get_id_only():
		noargs_id = [record.rec_id for record in search(app_inf['sink'])]
		print(noargs_id, '\n')
		noargs_id = [record.rec_id for record in search(app_inf['sink'], 'python')]
		pprint(_test_search(db_path=app_inf['sink'], show_only_id=True))
		print(noargs_id, '\n')
		noargs_id = [record.rec_id for record in search(app_inf['sink'], 'python', 1501259124168000)]
		print(noargs_id, '\n')
		noargs_id = [record.rec_id for record in search(app_inf['sink'], 'python', 1501259124168000, 1509123590555000)]
		print(noargs_id, '\n')

	root = Path(__file__).parents[2]
	db_test = str(root.joinpath('tests\\data\\db_for_testing_search.sqlite'))
	db_main = str(root.joinpath('db_merge\\all_merged.sqlite'))

	queries = [
			# 'checkio', # works
			#  'python game NOT javascript', # works
			#  '"java" *', # works
			# '* "java"', # doesnt work
			# 'script',  # works
			# 'python OR NEAR(pep list)', # works
			# 'python OR (NEAR (pep hacker) list)', # works
			# 'python OR (NEAR (pep hacker) AND list)', # works
			# 'python OR  (pep hacker) list', # doesnt work
			# 'python OR (pep hacker) AND list', # works
			# 'python OR NEAR(pep hacker) alist', # works
			# '(pep hacker) list',  # doesn't work
			# '(pep hacker) OR list', # works
			# 'python OR (pep hacker)   NOT     list', # works
			# 'NOT(pep hacker)',  # doesn't work
			# 'python OR javascript NOT  ((abacus hacker) fortran)', # doesn't work
			]

	# print(search(app_inf['sink']))
	# _test(queries=queries,db_test=db_test)
	# pprint(search(app_inf['sink'], 'python'))
	with sqlite3.connect(app_inf['sink']) as sink_conn:
		pprint(search(sink_conn, 'python import'))
	# _test_search(app_inf['sink'], 'python')
