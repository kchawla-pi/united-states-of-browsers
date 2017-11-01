# -*- encoding: utf-8 -*-
import os

from array import array
from bisect import insort
from collections import OrderedDict as odict

from united_states_of_browsers.db_merge import helpers

from united_states_of_browsers.db_merge.imported_annotations import *


def setup_output_db_paths(output_db: Optional[Text]) -> [PathInfo, PathInfo]:
	'''
	 Returns paths for the database file and the file with record of processed record's hashes.
	 Accepts filename.ext for the database file to be written to.
	'''
	if output_db:
		try:
			output_db, output_ext = output_db.split(os.extsep)
		except ValueError:
			output_ext = 'sqlite'
		sink_db_path = helpers.filepath_from_another(os.extsep.join([output_db, output_ext]))
		url_hash_log_filename = '_'.join([os.path.splitext(output_db)[0], 'url_hash_log.bin'])
	else:
		import datetime
		this_moment = str(datetime.datetime.now()).split('.')[0]
		this_moment = this_moment.replace('-', '')
		this_moment = this_moment.replace(':', '')
		this_moment = this_moment.replace(' ', '_')
		url_hash_log_filename = '_'.join(['url_hash_log.bin', this_moment])
		sink_db_path = None
		
	url_hash_log_path = helpers.filepath_from_another(url_hash_log_filename)
	return sink_db_path, url_hash_log_path


if __name__ == '__main__':
	test_records = (
		{47356370932282: odict(
				[('id', 1), ('url', 'https://www.mozilla.org/en-US/firefox/central/'),
				 ('title', None), ('rev_host', 'gro.allizom.www.'), ('visit_count', 0),
				 ('hidden', 0), ('typed', 0), ('favicon_id', None), ('frecency', 74),
				 ('last_visit_date', None), ('guid', 'NNqZA_f2KHI1'), ('foreign_count', 1),
				 ('url_hash', 47356370932282), ('description', None), ('preview_image_url', None)])},
		{47357795150914: dict(odict(
				[('id', 2), ('url', 'https://support.mozilla.org/en-US/products/firefox'),
				 ('title', None), ('rev_host', 'gro.allizom.troppus.'), ('visit_count', 0),
				 ('hidden', 0), ('typed', 0), ('favicon_id', None), ('frecency', 74),
				 ('last_visit_date', None), ('guid', '4xhwpotXndUs'), ('foreign_count', 1),
				 ('url_hash', 47357795150914), ('description', None), ('preview_image_url', None)]))},
		)
	import jsonlines
	# for record in test_records:
		# write_to_json('example_json.jsonl', record)
	with jsonlines.open('example_json.jsonl', 'w') as json_records_obj:
		for record in test_records:
			json_records_obj.write(record)
