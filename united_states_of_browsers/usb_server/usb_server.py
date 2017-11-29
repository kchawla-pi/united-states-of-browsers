# -*- encoding: utf-8 -*-
import json
import os
from pathlib import Path
import sqlite3

from flask import (Flask,
                   g,
                   render_template,
                   )


app = Flask(__name__)
app.config.from_object(__name__)

app_root_path = Path(app.root_path).parents[0]
app_inf_path = app_root_path.joinpath('db_merge', 'app_inf.json')

with open(str(app_inf_path), 'r') as json_obj:
	app_inf = json.load(json_obj)

app.config.update(dict(
		DATABASE=str(app_inf['sink']),
		SECRET_KEY='development key',
		USERNAME='admin',
		PASSWORD='default',
		DEBUG=True,
		))
app.config.from_envvar('USB_SERVER_SETTINGS', silent=True)


def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
		return g.sqlite_db
		

def connect_db():
		conn = sqlite3.connect(app.config['DATABASE'])
		conn.row_factory = sqlite3.Row
		return conn


@app.route('/')
def show_entries():
	db = get_db()
	select_query = '''SELECT url, title,visit_count, last_visit_date, description FROM search_table'''
	cur = db.execute(select_query)
	entries = cur.fetchmany(1000)
	# entries = (record for record in cur)
	return render_template('main.html', entries=entries)
	

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
	

def run_flask():
	app.run()


if __name__ == '__main__':
	run_flask()


