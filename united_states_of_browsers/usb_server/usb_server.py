# -*- encoding: utf-8 -*-
import os
import sqlite3

from flask import (Flask,
                   g,
                   render_template,
                   )


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
		DATABASE=os.path.realpath(os.path.join(app.root_path, '..', 'db_merge', 'all_merged.sqlite')),
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
	return render_template('ui_draft.html', entries=entries)
	

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
	

def run_flask():
	app.run()


if __name__ == '__main__':
	run_flask()


