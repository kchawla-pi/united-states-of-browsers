import shutil
import sqlite3
import tempfile

from pathlib import Path


class TemporaryCopy:
	def __init__(self, original_file):
		self.original_file = Path(original_file)
		self.temp_db = None

	def __enter__(self):
		filename = Path(self.original_file).name
		tempdir = Path(__file__).parents[1].joinpath('appdata', 'temp')
		tempfile.mkdtemp(tempdir)
		self.temp_db = tempdir.joinpath(filename)
		shutil.copy2(self.original_file, self.temp_db)
		yield self.temp_db

	def __exit__(self):
		shutil.rmtree(self.temp_db)



def connect(path):
	with sqlite3.connect(str(path)) as conn:
		conn.row_factory = sqlite3.Row
		yield conn
