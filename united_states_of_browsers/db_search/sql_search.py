
# for val in conn.execute('pragma compile_options'):
# 	print(val)


def off(conn):
	# conn.execute("DROP table history;")
	#
	# conn.execute("CREATE virtual table history USING fts5(url, title, url_hash);")
	# conn.executescript("""
	# 	INSERT INTO history (url, title, url_hash) VALUES ('www.google.com', 'Google', '1234');
	# 	INSERT INTO history (url, title, url_hash) VALUES ('www.yahoo.com', 'Yahoo', '2345');
	# 	""")
	# for row in conn.execute("SELECT url, title, url_hash FROM history WHERE history MATCH 'title:yahoo';"):
	# 	print(row)
	pass

	# conn.enable_load_extension(False)
# off(conn)
# conn.enable_load_extension(True)

import sqlite3

from collections import namedtuple, OrderedDict as odict
from pathlib import Path
from pprint import pprint
import datetime
import time


db_path = Path(__file__).parents[2].joinpath('full_history_merged_db.sqlite')
conn = sqlite3.connect(str(db_path))


conn.row_factory = sqlite3.Row
query_result = conn.execute("""SELECT * FROM moz_places""")
print(query_result.fetchone().keys())
record1 = dict(query_result.fetchone())


print(record1['last_visit_date'])
# print(datetime.datetime.fromordinal((record1['last_visit_date'])))
print(datetime.datetime.utcfromtimestamp(record1['last_visit_date']/1e3))
# for record in query_result:
# 	pass
	# print(record.keys())
	# print(odict(record))
	
