# -*- encoding: utf-8 -*-
import sqlite3
import os

from db_merge.annotations import *


def connect_db(db_file: Path) -> dict:
	"""
	Establishes connection to the database file, returns connection, cursor objects and filename.
	Accepts path of the database file.
	"""
	conn = sqlite3.connect(database=db_file)
	cur = conn.cursor()
	db_connection_info = {'connection': conn,
	                      'cursor': cur,
	                      'dbfile': os.path.split(db_file)[1],
	                      }
	return db_connection_info


def _db_tables(cursor: sqlite3.Connection.cursor) -> List[str]:
	"""
	Returns names of tables in database.
	Accepts cursor object of the database file.
	"""
	query = "SELECT name FROM sqlite_master WHERE type = 'table'"
	return [table_[0] for table_ in cursor.execute(query)]



