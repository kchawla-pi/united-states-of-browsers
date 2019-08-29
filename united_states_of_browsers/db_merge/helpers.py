from pathlib import Path
from typing import Text, Sequence, Dict, Union, Iterable


def make_queries(tablename: Text, primary_key_name: Text, fieldnames: Sequence[Text]) -> Dict:
	""" Constructs the queries necessary for specific purposes.
	Returns them as dict['purpose': 'query']
	"""
	fieldnames_str = ', '.join(fieldnames)
	query_placeholder = '?, ' * len(fieldnames)
	queries = {'create': f'''CREATE TABLE IF NOT EXISTS {tablename} ({primary_key_name} integer PRIMARY KEY, {fieldnames_str[:]})'''}
	queries.update({'insert': f"INSERT INTO {tablename}({fieldnames_str}) VALUES ({query_placeholder[:-2]})"})
	return queries


def query_sanitizer(query: str, allowed_chars: Union[str, Iterable]='_') -> str:
	""" Removes non-alphanumeric characters from a query.
	Retains characters passed in via `allowed_chars`. (Default: '_')
	Returns a string.
	"""
	allowed_chars = set(allowed_chars)
	return ''.join([char for char in query if char.isalnum() or char in allowed_chars])  #, '?', '(', ')', ','}])


def get_root_path(project_file_path, project_root_dir_name):
	path_parts = Path(project_file_path).parts
	try:
		root_dir_idx = path_parts.index(project_root_dir_name)
	except ValueError:
		error_text = f'Project root directory name "{project_root_dir_name}" not present in supplied path', project_root_dir_name, project_file_path
		raise ValueError(error_text)
	project_root_path = Path(*path_parts[:root_dir_idx+1])
	return f'{project_root_path}'
