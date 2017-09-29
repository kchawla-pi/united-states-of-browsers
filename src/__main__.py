import read_browser_db


file_paths = read_browser_db.firefox()
prepped_records = read_browser_db.read_browser_db(filepaths=file_paths)
for profile_count, data_in_profile in enumerate(prepped_records):
	print('\n' * 2)
	print('profile count:', profile_count)
	input()
	for record_count, record in enumerate(data_in_profile ):
		print('record_count', record_count)
		print(record)
