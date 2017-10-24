import sqlite3


def quick_read_record(database, how_many=10):
	conn = sqlite3.connect(database)
	cur = conn.cursor()
	query = '''SELECT * FROM {}'''.format('moz_places')
	cur.execute(query)
	print_more = None
	print(cur.description)
	for count, record in enumerate(cur):
		print(record[-3])
		print(record)
		if count % how_many == 0:
			print_more = input()
		if print_more:
			break


def print_records(record_gen, each_time=10, profile_name=None):
	import time
	if profile_name:
		print('\n' * 2, profile_name, '\n' * 2)
	time.sleep(2)
	print('Press ENTER key for the next set of records, c for number of records so far, any other to exit.\n\n')
	time.sleep(1)
	for srn, record in enumerate(record_gen):
		print(record)
		try:
			cond = srn % each_time == 0 and srn > 0
		except TypeError:
			pass
		else:
			if cond:
				quitter = input()
				if quitter in {'c', 'C'}:
					print(srn)
					time.sleep(1)
				elif quitter:
					break
				pass


def show_record_(record, record_count, each_time=100, profile_name=None):
	if each_time:
		import time
		prev_iter_profile_name = ''
		if profile_name and profile_name == prev_iter_profile_name:
			print('\n' * 2, profile_name, '\n' * 2)
			time.sleep(2)
		
		print(record_count, record)
		try:
			cond = record_count % each_time == 0 and record_count > 0
		except TypeError:
			pass
		except ZeroDivisionError:
			pass
		else:
			if cond:
				quitter = input('\nPress ENTER key for the next set of records, c for number of records so far, any other to exit.\n\n')
				if quitter in {'c', 'C'}:
					print(record_count)
					time.sleep(1)
				elif quitter:
					quit()
				pass
		prev_iter_profile_name = profile_name

# def test_print_records(cursor, table, prepped_records):
# 	from united_states_of_browsers.db_merge import write_new_db
# 	for num1, record in enumerate(prepped_records):
# 		query = '''SELECT * FROM {}'''.format('moz_places')
# 		cursor.execute(query)
# 		for num2, record__ in enumerate(cursor):
# 			if num2 == 37:
# 				print(num2)
# 				print(record__)
# 				break
#
# 		print('-')
# 		if num1 == 37:
# 			print(num1)
# 			write_new_db.write_to_db(sink_db_info='test.sqlite', record=record, table=table)
# 			print('wriiten')
# 			break
