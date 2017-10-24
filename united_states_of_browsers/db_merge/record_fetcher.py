# -*- encoding: utf-8 -*-
import sqlite3

from united_states_of_browsers.db_merge.imported_annotations import *
from united_states_of_browsers.db_merge.helpers import safetychecks


def _table_records(cursor, table: [str, Sequence[str]]) -> Generator:
	"""
	Yields one record (row) of the table, whenever called.
	Accepts the db connection cursor and table name

	"""
	safetychecks(table)
	sort_key = "url_hash"
	query = '''SELECT * FROM {} ORDER BY {}'''  .format(table, sort_key)
	try:
		cursor.execute(query)
	except sqlite3.OperationalError:
		return Exception(table)
	else:
		field_names = [desc_[0] for desc_ in cursor.description]
		yield field_names
		for record_ in cursor:
			yield record_


def _make_records_dict_generator(records: Iterable, record_template: Dict) -> Generator:
	'''
	Yields a dict with field names: field data as key: value pairs
	Accepts record yielding generator and a dict with field names as keys.
	'''
	fieldnames = next(records)
	for record_ in records:
		record_template.update({fieldname_: field_
		       for fieldname_, field_ in zip(fieldnames, record_)})
		yield {record_template['url_hash']: record_template.copy()}


def yield_prepped_records(*, cursor, table: str, record_template: Dict) -> Generator:
	'''
	Returns a generator of of generator of database records. (i know I know. Working on it.)
	Accepts connection cursor, table name and record template ({fieldnames: None})
	'''
	records = _table_records(cursor=cursor, table=table)
	try:
		raise records  # if records is exception, rest mustn't happen
	except TypeError:
		prepped_records_generator = _make_records_dict_generator(records=records,
		                                                         record_template=record_template)
		return prepped_records_generator
