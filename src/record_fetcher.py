import sqlite3

from collections import OrderedDict as odict


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


def _make_records_dict_generator(records: 'iterable', table=None, filepath=None):
	record_dict = [odict({'_filepath': filepath, 'table': table})]
	# pprint(list(records))
	# quit()
	field_names = next(records)
	for record_ in records:
		yield {field_name_: field_
		       for field_name_, field_ in zip(field_names, record_)}
	# return record_dict


def yield_prepped_records(*, cursor, table, filepath):
	records = _table_records(cursor=cursor, table=table)
	try:
		raise records  # if records is exception, rest mustn't happen
	except TypeError:
		prepped_records_generator = _make_records_dict_generator(records=records, table=table,
		                                                         filepath=filepath)
		return prepped_records_generator
