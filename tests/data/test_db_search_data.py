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
		]
		
	return search_testdata


search_testdata = data_for_search()
# pprint(search_testdata['keywords only'])
# for elem in [test_case for test_case in search_testdata['keywords only']]:
# 	print(elem)
