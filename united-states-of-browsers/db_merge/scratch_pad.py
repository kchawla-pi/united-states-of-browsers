'''
A place for experimentation and playing with new concepts and ideas. Not included in the actual finished code.
'''
keys = {
	8470: ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'favicon_id', 'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description', 'preview_image_url'],
	8471: ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'favicon_id', 'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description', 'preview_image_url'],
	8472: ['id', 'url', 'title', 'rev_host', 'visit_count', 'hidden', 'typed', 'frecency', 'last_visit_date', 'guid', 'foreign_count', 'url_hash', 'description', 'preview_image_url'],

	}

import os
filepath_from_another = lambda *filename, filepath=__file__: os.path.realpath(os.path.join(os.path.dirname(filepath), *filename))

print(filepath_from_another('output', 'abc.txt'))
print(filepath_from_another('output', 'try', 'abc.txt'))
print(filepath_from_another('output', 'try', 'abc.txt', filepath='C:'))


def fpfa(filepath=__file__, *filename):
	filepath_dir = os.path.dirname(filepath)
	filepath = os.path.join(*filepath)
	return os.path.realpath(os.path.join(filepath_dir, filepath))
	
print()
print(fpfa())
print(fpfa('abc.txt'))
print(fpfa('output', 'abc.txt'))
print()

filepath_from_another = lambda filepath=__file__, *filename: os.path.realpath(os.path.join(os.path.dirname(filepath), *tuple(filename)))

# print(filepath_from_another())
print(filepath_from_another('abc.txt'))
print(filepath_from_another('output', 'abc.txt'))
# print(filepath_from_another('output', 'try', 'abc.txt', filepath='C:'))


