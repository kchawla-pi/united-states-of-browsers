# -*- encoding: utf-8 -*-
import json
import sqlite3
import werkzeug

from pathlib import Path
from flask import (Flask,
                   g,
                   render_template,
                   request,
                   )

from united_states_of_browsers.db_merge import db_search
from united_states_of_browsers.db_merge.paths_setup import app_inf_path

app = Flask(__name__)
app.config.from_object(__name__)

app_root_path = Path(app.root_path).parents[0]

with open(app_inf_path, 'r') as json_obj:
	app_inf = json.load(json_obj)

app.config.update(dict(
		DATABASE=app_inf['sink'],
		SECRET_KEY='development key',
		USERNAME='admin',
		PASSWORD='default',
		DEBUG=True,
		LOGGING_LOCATION=app.root_path+'error.log',
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


@app.route('/', methods=['GET', 'POST'])
def show_entries():
	db = get_db()
	select_query = '''SELECT url, title,visit_count, last_visit_date_readable FROM search_table'''
	cur = db.execute(select_query)
	entries = cur.fetchmany(1000)
	return render_template('main.html', entries=entries )


@app.route('/search', methods=['GET', 'POST'])
def search():
	db = get_db()
	search_results = db_search.search(db,
	                                  request.args["query"],
	                                  request.args["date-from"],
	                                  request.args["date-to"]
	                                  )

	return render_template('main.html', entries=search_results)
	# return search_results

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
	

def run_flask():
	app.run()


if __name__ == '__main__':
	run_flask()


