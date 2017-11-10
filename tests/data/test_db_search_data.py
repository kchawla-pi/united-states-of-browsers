from collections import namedtuple


TestFields = namedtuple('TestFields', 'title url url_hash guid')
TestCase = namedtuple('TestCase', 'input expected')


def get_searches_list ():
	entered_queries = ('python pep list',
	                   'python, pep, list,',
	                   'python pep list -machine',
	                   'python pep list -(machine learning)',
	                   'python pep list NOT machine',
	                   'python pep list NOT (machine learning)',
	                   'python pep OR list NOT (machine learning)',
	                   'python OR (pep list) NOT (machine learning)',
	                   'python OR (pep, list) NOT (machine, learning)',
	                   'python AND ("machine learning" OR numpy) NOT (pep list)',
	                   )
	search_queries = ('title:python',
	                  'title:python AND variable NOT update NOT anaconda',
	                  'title:python AND variable',
	                  'title:python AND variable NOT update',
	                  'title:python AND variable NOT (update, Anaconda)',
	                  'title:python AND variable NOT (update Anaconda)',
	                  'title:python AND variable NOT(update Anaconda)',
	                  'title:python AND variable NOT update Anaconda)',
	                  'title:python AND variable NOT update Anaconda',
	                  'title:python AND variable NOT update ',
	                  'title:python AND variable NOT update not anaconda',
	                  'title:python AND variable NOT update NOT anaconda',
	                  'title:python AND variable NOT update NOT anaconda url:stackoverflow',
	                  'title:python AND variable NOT update NOT anaconda url:*stackoverflow*',
	                  'title:python AND variable NOT update NOT anaconda url:*stackoverflow',
	                  'title:python AND variable NOT update NOT anaconda url:stackoverflow',
	                  'title:python AND variable NOT update NOT anaconda AND url:stackoverflow',
	                  'python AND variable NOT update NOT anaconda AND stackoverflow',
	                  'python AND variable NOT update - anaconda AND stackoverflow',
	                  'python AND variable NOT update \- anaconda AND stackoverflow',
	                  'python AND variable NOT update "- anaconda AND stackoverflow',
	                  "python AND variable NOT update '- anaconda AND stackoverflow",
	                  )
	return entered_queries, search_queries


def data_for_search ():
	global TestCase, TestFields
	search_testdata = dict.fromkeys(
			['keywords only', 'keywords+both dates', 'keywords+start date', 'keywords+end date'],
			None)
	
	search_testdata['keywords only'] = [
		TestCase(input='twitter',
		         expected=[TestFields(title='Franz Support on Twitter: "We are working on an update '
		                                    'to improve the stability of Franz. More infos coming soon. 🎅🏻"',
			                    url='https://twitter.com/franzsupport/status/810975463480979456?lang=en',
			                    url_hash=47357899617728, guid='riB9LFRxrW_C')
			         ]
		         ),
		TestCase(input='franz',
		         expected=[TestFields(title='Franz Support on Twitter: "We are working on an update '
			                          'to improve the stability of Franz. More infos coming soon. 🎅🏻"',
			                    url='https://twitter.com/franzsupport/status/810975463480979456?lang=en',
			                    url_hash=47357899617728, guid='riB9LFRxrW_C')
			         ]
		         ),
		TestCase(input='javascript python NOT react',
		         expected=[TestFields(title='CheckIO - online game for Python and JavaScript coders',
		                              url='https://checkio.org/',
		                              url_hash=47358795098781, guid='LQhtEHjQYW9O')
		                   ]
		         ),
		TestCase(input='python',
		         expected=[
			         TestFields(title='CheckIO - online game for Python and JavaScript coders',
			                    url='https://checkio.org/', url_hash=47358795098781,
			                    guid='LQhtEHjQYW9O'),
			         TestFields(title=None,
			                    url='https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&ved=0ahUKEwi0lLWK9e_VAhXEMSYKHQB-DLwQFgg6MAI&url=https%3A%2F%2Fwww.python.org%2Fjobs%2F&usg=AFQjCNGVN2EMfuOJtnlD7PnKYT4CJwTCpg',
			                    url_hash=47360571611328, guid='6tqwfOD2rnhn'),
			         TestFields(title='Create a Python game: how to make a puzzle game called Same - The MagPi MagazineThe MagPi Magazine',
			                    url='https://www.raspberrypi.org/magpi/create-python-game/',
			                    url_hash=47359990351841, guid='hJUUonA35KiM'),
			         TestFields(title="python - How to import module when module name has a '-' dash or hyphen in it? - Stack Overflow",
			                    url='https://stackoverflow.com/questions/8350853/how-to-import-module-when-module-name-has-a-dash-or-hyphen-in-it',
			                    url_hash=47358360613425, guid='-t4Ztj7fmHYC'),
			         TestFields(title='Learn Python the Hard Way',
			                    url='https://learnpythonthehardway.org/python3/appendix-a-cli/introduction.html',
			                    url_hash=47356852294123, guid='lKsnTf4niVxn'),
			         TestFields(title='Top 6 Open Source Python Application Servers',
			                    url='https://blog.idrsolutions.com/2015/05/top-6-open-source-python-application-servers/',
			                    url_hash=47359959715876, guid='cr4KtxIMCg0r'),
			         TestFields(title='Python Developer, Groom & Associates | Python.org',
			                    url='https://www.python.org/jobs/2626/', url_hash=47356330220911,
			                    guid='uUVQa0s1vg_U'),
			         TestFields(title='Python Cookbook',
			                    url='http://chimera.labs.oreilly.com/books/1230000000393/ch06.html#_discussion_95',
			                    url_hash=125510013275591, guid='Zlo9LP2OWH65'),
			         TestFields(title='Browse : Python Package Index',
			                    url='https://pypi.python.org/pypi?:action=browse&c=4',
			                    url_hash=47360326338850, guid='QLnAxVpUWyx4'),
			         TestFields(title='Rmotr advanced-python-programming-syllabus.pdf',
			                    url='https://mail-attachment.googleusercontent.com/attachment/u/0/?ui=2&ik=0dcb9da7ee&view=att&th=15e717fed6ab522e&attid=0.1&disp=safe&zw&saddbat=ANGjdJ9yCEWJ5KM1NGQXNJORW-x6Kn69_KkPVhGkW2NAxXn_PjwZUpx2YmYVPYkoIfcBlpZR8B-MqyMelXDXcksTvB_HqTNYg0daXMrUklqd7JtmVRVjbLThcte0GfoEQ4kEyCsHvwk3ExGxSkuIB0sdH7GpEXjq4HqzmStvvOqvKeEl_-eLXvRUXgkGho6CgbxLUJBlQFJ7paPRDvWvJO95BdnMOiGdjDCnljFpImEwNcrgJoK9FyAkYpV0l9wRfIL3DMQ5oeEnlMhveaPxND8c1_Cp9GTNBc90yBRYpJ3388h8y8FtdeUCcGUV8S0WePrDnk86CYBll7K8vkKBI2089AAB_JEW3C35j2Sy47IumbyUc7HoEVofT4-aLZCAUu_VxsIDVJdgTC52nUfXWrBmOz-twglNMRKwFc3YmksIBk5XzqZF3uDqXlW4rDKfmhnl0iCySvycTQIKrz_TUBmC3JyHFIr4eFBGL0yak0dIe1x1zSR_0onr35QNtTv5pooMH34etPdzpVcJr8g4CunT2mTbGICO0X-tmyPk61a9BN8YJ4QzA-FW_OVOqTaImNX0iOPS6BRIjiJ3r5AYyL8-e09gV_9L0gX2hIzF3A',
			                    url_hash=47357624936213, guid='Umeftsoca4jQ'),
			         TestFields(title='generator - yield break in Python - Stack Overflow',
			                    url='https://stackoverflow.com/questions/6395063/yield-break-in-python',
			                    url_hash=47357668862239, guid='WTvQbT2rdjbU'),
			         ]
		
		         ),
		TestCase(input='python game NOT javascript',
		         expected=[TestFields(title='Create a Python game: how to make a puzzle game called '
		                                    'Same - The MagPi MagazineThe MagPi Magazine',
		                              url='https://www.raspberrypi.org/magpi/create-python-game/',
		                              url_hash=47359990351841, guid='hJUUonA35KiM')
		                   ]
		         ),
		
		# 'title:7 OR url:7 OR description:7'
		# TestCase(input='7',
		#          expected=[(5849, 'https://smile.amazon.com/dp/B06XHB6BLN?psc=1',
		#                     'AmazonSmile: Sardonyx SX-918 Bluetooth Headphones, Best Wireless Sport Earphones Noise Cancelling IPX7 Waterproof HD Stereo Headset w/ Mic, Secure-Fit Sweatproof Earbuds for Gym Running Workout Exercise: Cell Phones & Accessories',
		#                     'moc.nozama.elims.', 1, 0, 0, None, 20, 1499536336654000,
		#                     'UVWj0HGn5qbR', 0, 47359401703531, None, None),
		#                    (10008,
		#                     'https://www.amazon.com/Grokking-Algorithms-illustrated-programmers-curious/dp/1617292230/ref=sr_1_cc_5?s=aps&ie=UTF8&qid=1503858154&sr=1-5-catcorr&keywords=complete+guide+to+programmer',
		#                     'Grokking Algorithms: An illustrated guide for programmers and other curious people: Aditya Bhargava: 4708364241294: Amazon.com: Books',
		#                     'moc.nozama.www.', 1, 0, 0, None, 20, 1503858165373000, 'TvQcaACHe5G5',
		#                     0, 47358489321016, None, None),
		#                    (7787, 'https://notepad-plus-plus.org/download/v7.5.html',
		#                     'Notepad++ v7.5 - Current Version', 'gro.sulp-sulp-dapeton.', 1, 0, 0,
		#                     None, 84, 1503613295245000, 'Bii_6pC2Xti-', 0, 47360402797294, None,
		#                     None)
		#                    ]
		#          ),
		]
	
	return search_testdata


search_testdata = data_for_search()
# pprint(search_testdata['keywords only'])
# for elem in [test_case for test_case in search_testdata['keywords only']]:
# 	print(elem)
