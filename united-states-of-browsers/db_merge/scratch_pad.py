import os
import sqlite3

from pathlib import Path


db_file = Path(os.path.dirname(__file__), 'merged_fx_db.sqlite')

# conn =
with sqlite3.connect(str(db_file)) as conn:
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	query = '''SELECT * FROM moz_places'''
	cur.execute(query)
	for row in cur:
		print(row)
		print(dict(row))
	
	
	# conn.close()
