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
