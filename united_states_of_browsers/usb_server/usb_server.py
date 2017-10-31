import os
import sqlite3
import subprocess

from flask import (Flask,
                   g,
                   render_template,
                   )


app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
		DATABASE=os.path.realpath(os.path.join(app.root_path, '..', 'db_merge_v1', 'merged_fx_db.sqlite')),
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
	select_query = '''SELECT * FROM moz_places'''
	cur = db.execute(select_query)
	entries = cur.fetchmany(10)
	return render_template('show_records.html', entries=entries)
	
	
@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
	

def run_flask():
	app.run()
	# subprocess.run(['set', 'FLASK_APP', '=', 'usb_server'])
	# subprocess.run(['set', 'FLASK_DEBUG=true'])
	# subprocess.run(['python', 'flask', 'run'])


if __name__ == '__main__':
	run_flask()



pass

