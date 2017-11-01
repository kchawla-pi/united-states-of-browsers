import pytest
import sqlite3

from collections import OrderedDict as odict
from pathlib import Path

from united_states_of_browsers.db_merge_v1 import merge_browser_databases


home_dir = Path.home()
profile_dbs = {'test_profile0':
	               f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite',
               'test_profile1':
	               f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite',
               'test_profile2':
	               f'{home_dir}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
               }


def establish_benchmark(profile_dbs):
	profile_records_dict = odict()
	for profile_name, profile_path in profile_dbs.items():
		conn = sqlite3.connect(profile_path)
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()
		query = '''SELECT * FROM moz_places'''
		try:
			cur.execute(query)
		except sqlite3.OperationalError:
			pass
		else:
			profile_records_dict.update({profile_name: [dict(row) for row in cur]})
		finally:
			conn.close()
	merged_as_dict = odict({
				info['url_hash']: odict(info)
				for profile_info in profile_records_dict.values()
				for info in profile_info
		})
	return merged_as_dict


merged_url_hashes, merged_using_usb = merge_browser_databases.merge(profiles=profile_dbs.keys())
benchmark_merged_dict = establish_benchmark(profile_dbs)

print(len(merged_using_usb))
print(len(benchmark_merged_dict))

@pytest.mark.parametrize(('usb_merged_elem', 'benchmark_merged_elem'), [(merged_using_usb[url_hash], benchmark_merged_dict[url_hash]) for url_hash in merged_using_usb])
def test_merge(usb_merged_elem, benchmark_merged_elem):
		if 'place:' not in usb_merged_elem['url']:
			for field in usb_merged_elem:
				bench_info = benchmark_merged_elem.get(field, None)
				actual_info = usb_merged_elem.get(field, None)
				are_same = bench_info==actual_info
				if not are_same:
					print(field, ':', bench_info, actual_info, are_same)
				assert are_same
