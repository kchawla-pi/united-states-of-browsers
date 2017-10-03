import sqlite3

from helpers import safetychecks


# from write_new_db import safetychecks

def _table_records(cursor, table):
	"""
	Yields one record (row) of the table, whenever called.

	Usage:
		table_records_generator = _table_records(cursor, table)
		next_record_in_table = next(table_records_generator)
	:param cursor: Cursor object for current database file
	:type cursor: Connection.Cursor object
	:param table: Name of table
	:type table: str
	:return: Yields tuple of record, each column separated by a comma
	:rtype: tuple[str, *str, ...]
	"""
	safetychecks(table)
	query = '''SELECT * FROM {}'''.format(table)
	try:
		cursor.execute(query)
	except sqlite3.OperationalError:
		return Exception(table)
	else:
		field_names = [desc_[0] for desc_ in cursor.description]
		yield field_names
		for record_ in cursor:
			yield record_


def _make_records_dict_generator(records: 'iterable', record_template):
	# record_dict = [odict({'_filepath': filepath, 'table': table})]
	fieldnames = next(records)
	for record_ in records:
		record_template.update({fieldname_: field_
		       for fieldname_, field_ in zip(fieldnames, record_)})
		yield {record_template['url_hash']: record_template}


def yield_prepped_records(*, cursor, table, filepath, record_template):
	records = _table_records(cursor=cursor, table=table)
	try:
		raise records  # if records is exception, rest mustn't happen
	except TypeError:
		# field_names = next(records)
		prepped_records_generator = _make_records_dict_generator(records=records,
		                                                         record_template=record_template)
		return prepped_records_generator
