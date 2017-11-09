from collections import namedtuple
from pathlib import Path
from pprint import pprint

from united_states_of_browsers.db_merge.database_operations import DBRecord


def get_searches_list():
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

def data_for_search():
	TestCase = namedtuple('TestCase', 'input expected')
	search_testdata = dict.fromkeys(['keywords only', 'keywords+both dates', 'keywords+start date', 'keywords+end date'], None)
	
	search_testdata['keywords only'] = [
		TestCase(input='twitter',
		         expected=[(455, 'https://twitter.com/franzsupport/status/810975463480979456?lang=en',
		                   'Franz Support on Twitter: "We are working on an update to improve the '
		                   'stability of Franz. More infos coming soon. 🎅🏻"', 'moc.rettiwt.', 1, 0,
		                   0, None, 78, 1501449040291000, 'riB9LFRxrW_C', 0, 47357899617728, None,
		                   None
		                   )]
		         ),
		TestCase(input='franz',
		         expected=[(455, 'https://twitter.com/franzsupport/status/810975463480979456?lang=en',
				         'Franz Support on Twitter: "We are working on an update to improve the '
				         'stability of Franz. More infos coming soon. 🎅🏻"', 'moc.rettiwt.', 1, 0,
				         0, None, 78, 1501449040291000, 'riB9LFRxrW_C', 0, 47357899617728, None,
				         None)]
		         ),
		# 'title:7 OR url:7 OR description:7'
		TestCase(input='7*',
		         expected=[(5849, 'https://smile.amazon.com/dp/B06XHB6BLN?psc=1',
		                    'AmazonSmile: Sardonyx SX-918 Bluetooth Headphones, Best Wireless Sport Earphones Noise Cancelling IPX7 Waterproof HD Stereo Headset w/ Mic, Secure-Fit Sweatproof Earbuds for Gym Running Workout Exercise: Cell Phones & Accessories',
		                    'moc.nozama.elims.', 1, 0, 0, None, 20, 1499536336654000,
		                    'UVWj0HGn5qbR', 0, 47359401703531, None, None),
		                   (10008,
		                    'https://www.amazon.com/Grokking-Algorithms-illustrated-programmers-curious/dp/1617292230/ref=sr_1_cc_5?s=aps&ie=UTF8&qid=1503858154&sr=1-5-catcorr&keywords=complete+guide+to+programmer',
		                    'Grokking Algorithms: An illustrated guide for programmers and other curious people: Aditya Bhargava: 4708364241294: Amazon.com: Books',
		                    'moc.nozama.www.', 1, 0, 0, None, 20, 1503858165373000, 'TvQcaACHe5G5',
		                    0, 47358489321016, None, None),
		                   (7787, 'https://notepad-plus-plus.org/download/v7.5.html',
		                    'Notepad++ v7.5 - Current Version', 'gro.sulp-sulp-dapeton.', 1, 0, 0,
		                    None, 84, 1503613295245000, 'Bii_6pC2Xti-', 0, 47360402797294, None,
		                    None)
		                   ]
		         ),
		]
		
	return search_testdata


search_testdata = data_for_search()
# pprint(search_testdata['keywords only'])
# for elem in [test_case for test_case in search_testdata['keywords only']]:
# 	print(elem)
