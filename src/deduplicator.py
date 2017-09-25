#:TODO: Algorithm.
'''
{prologue: File with url_hash: id}
0. Open Source DB from Profile. - Done in read_browser_db()
1. Open Sink DB. - Done in write_new_db()
2. Fetch source record from Profile. - Done in read_browser_db()
3. Open URL Archive.
4. Get url_hash
5. check if URL hash in archive.
 - If Yes, Update Last Visited & Visit counts using primary key id, or url_hash.
 - If No, Change id to next available value, write the record to sink. Add {url_hash: id} to archive.
6. Commit.
7. Open next profile.
8. Repeat.
Close Source & Sink DBs.

'''
def open_url_hash_log():
	'''
	Open the archive, load url_hashes (keys) from it as a set.
	:return: set of url hashes
	'''
	# Open url_hash archive.
	pass


def redundant_url_hash(record):
	'''
	Reads the url_hash & id field from record, membership test with archive set.
	Returns {url_hash: id} or None
	:param record:
	'''
	pass


def update_record(record, cursor):
	'''
	Finds existing record in Sink DB using hash_val or id.
	Updates last visited to latest, adds the visit counts.
	:param record:
	:type record:
	:return:
	:rtype:
	'''
	pass


def insert_record(record):
	'''
	Changes record id to next available.
	:param record: record
	:type record:
	:return:
	:rtype:
	'''
	
# save/commit changes.
