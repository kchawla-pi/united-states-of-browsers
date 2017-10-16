from db_merge.deduplicator import deduplicate_records


def test_deduplicate_records():
	test_records = [
		{47356370932282:
			 {'id': 1, 'url': 'https://www.mozilla.org/en-US/firefox/central/', 'title': None,
			  'rev_host': 'gro.allizom.www.', 'visit_count': 10, 'hidden': 0, 'typed': 0,
			  'favicon_id': None, 'frecency': 76, 'last_visit_date': 1503579273203000,
			  'guid': 'NNqZA_f2KHI1',
			  'foreign_count': 1, 'url_hash': 47356370932282, 'description': None,
			  'preview_image_url': None}
		 },
		{47357795150914:
			 {'id': 2, 'url': 'https://support.mozilla.org/en-US/products/firefox', 'title': None,
			  'rev_host': 'gro.allizom.troppus.', 'visit_count': 20, 'hidden': 0, 'typed': 0,
			  'favicon_id': None, 'frecency': 76, 'last_visit_date': 268505095842199,
			  'guid': '4xhwpotXndUs',
			  'foreign_count': 1, 'url_hash': 47357795150914, 'description': None,
			  'preview_image_url': None}
		 },
		{47357795150914:
			{'id': 2, 'url': 'https://support.mozilla.org/en-US/products/firefox',
			'title': None,
			'rev_host': 'gro.allizom.troppus.', 'visit_count': 2, 'hidden': 0,
			'typed': 0,
			'favicon_id': None, 'frecency': 76, 'last_visit_date': 1498227024629000,
			'guid': '4xhwpotXndUs',
			'foreign_count': 1, 'url_hash': 47357795150914, 'description': None,
			'preview_image_url': None}
		 },
		]

	expected_database = [
		{47356370932282:
			 {'id': 1, 'url': 'https://www.mozilla.org/en-US/firefox/central/', 'title': None,
			  'rev_host': 'gro.allizom.www.', 'visit_count': 10, 'hidden': 0, 'typed': 0,
			  'favicon_id': None, 'frecency': 76, 'last_visit_date': 268505095842199,
			  'guid': 'NNqZA_f2KHI1',
			  'foreign_count': 1, 'url_hash': 47356370932282, 'description': None,
			  'preview_image_url': None}
		 },
		{47357795150914:
			 {'id': 2, 'url': 'https://support.mozilla.org/en-US/products/firefox', 'title': None,
			  'rev_host': 'gro.allizom.troppus.', 'visit_count': 22, 'hidden': 0, 'typed': 0,
			  'favicon_id': None, 'frecency': 76, 'last_visit_date': None, 'guid': '4xhwpotXndUs',
			  'foreign_count': 1, 'url_hash': 47357795150914, 'description': None,
			  'preview_image_url': None}
		 },
		]
	returned_output = []
	for test_case in test_records:
		returned_output.append(deduplicate_records(test_case))
	print(returned_output)
	print('last_visit_date not fixed in one of the records. Test result invalid until it is.',
	      returned_output == expected_database)
