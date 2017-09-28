import sqlite3



def quick_read_record(database):
	conn = sqlite3.connect(database)
	cur = conn.cursor()
	query = '''SELECT * FROM {}'''.format('moz_places')
	cur.execute(query)
	for record in cur:
		print(record)
		
quick_read_record(database='test.sqlite')
