import itertools
import re

"""
# 'checkio', # works
#  'python game NOT javascript', # works
#  '"java" *', # works
# '* "java"', # doesnt work
# 'script',  # works
# 'python OR NEAR(pep list)', # works
# 'python OR (NEAR (pep hacker) list)', # works
# 'python OR (NEAR (pep hacker) AND list)', # works
# 'python OR  (pep hacker) list', # doesnt work
# 'python OR (pep hacker) AND list', # works
# 'python OR NEAR(pep hacker) alist', # works
# '(pep hacker) list',  # doesn't work
# '(pep hacker) OR list', # works
# 'python OR (pep hacker)   NOT     list', # works
"""

from collections import OrderedDict as odict


def standardize_query(query):
	query = ' '.join(query.split())
	for opener_idx, closer_idx in zip(('[', '{'), ('}', ']')):
		query = query.replace(opener_idx, '(')
		query = query.replace(closer_idx, ')')
	return query

def find_parantheses_indices(query):
	opener_indices = [idx for idx, char in enumerate(query) if char == '(']
	closer_indices = [idx for idx, char in enumerate(query) if char == ')']
	closer_indices.reverse()
	paran_pairs_indices = [(opener_idx, closer_idx) for opener_idx, closer_idx in
	                       zip(opener_indices, closer_indices)]
	return paran_pairs_indices


def improper_term_before_paranthesis (query, paranthesis_indices):
	terms_to_be_fixed = odict()
	operator_terms_presence = ('NOT', 'AND', 'OR')
	term_precedes_paranthesis = dict.fromkeys(operator_terms_presence, None)
	text_precedes_term = dict.fromkeys(operator_terms_presence, None)
	
	for term in term_precedes_paranthesis:
		before_paran_ = paranthesis_indices[0] - len(term)
		term_precedes_paranthesis[term] = term in query[before_paran_ - 1: paranthesis_indices[0]]
		text_precedes_term[term] = term_precedes_paranthesis[term] and query[:before_paran_]
		
		if term_precedes_paranthesis[term] and not text_precedes_term[term]:
			terms_to_be_fixed.update({paranthesis_indices: term})
	if terms_to_be_fixed:
		return terms_to_be_fixed


def improper_term_after_paranthesis(query, paranthesis_indices):
	terms_to_be_fixed = odict()
	operator_terms_presence = ('NOT', 'AND', 'OR')
	term_succeeds_paranthesis = dict.fromkeys(operator_terms_presence, None)
	text_succeeds_term = dict.fromkeys(operator_terms_presence, None)
	
	for term in term_succeeds_paranthesis:
		after_paran_ = paranthesis_indices[1] + len(term)
		term_succeeds_paranthesis[term] = term in query[paranthesis_indices[1]: after_paran_]
		text_succeeds_term[term] = query[after_paran_:]
		
		if term_succeeds_paranthesis[term] and not text_succeeds_term[term]:
			terms_to_be_fixed.update({paranthesis_indices: term})
		if not term_succeeds_paranthesis[term] and text_succeeds_term[term]:
			terms_to_be_fixed.update({paranthesis_indices: term})
	if terms_to_be_fixed:
		return terms_to_be_fixed


def create_test_data():
	queries_working = ['checkio',
	                   'python game NOT javascript',
	                   'python OR NEAR(pep list)',
	                   'python OR (NEAR (pep hacker) AND list)',
	                   'python OR (pep hacker) AND list',
	                   'python OR NEAR(pep hacker) AND list',
	                   '(pep hacker) OR list',
	                   ]
	queries_not_working = ['(pep hacker) list',
	                       '* "java"',
	                       'python OR javascript NOT  [[abacus hacker] fortran}']
	return queries_working, queries_not_working


if __name__ == '__main__':
	terms_to_be_fixed_preceding_paranthesis = []
	terms_to_be_fixed_succeeding_paranthesis = []
	
	queries_working, queries_not_working = create_test_data()
	# for queries in [queries_working, queries_not_working]:
	# for queries in queries_working:
	for queries in queries_not_working[-1:]:
		for query in [queries]:
			query = standardize_query(query)
			parantheses_indices = find_parantheses_indices(query)
			
			for paranthesis_indices_ in parantheses_indices:
				terms_to_be_fixed_preceding_paranthesis.append(improper_term_before_paranthesis(query, paranthesis_indices_))
				terms_to_be_fixed_succeeding_paranthesis.append(improper_term_after_paranthesis(query, paranthesis_indices_))
			print()
print()

	
"""
query_list = list(query)
query_list[opener_idx] = ' '
query_list[closer_idx] = ' '
query = ''.join(query_list)
print(query)
print()
# print(parantheses)
# acceptable_preceder_words =
WHY not just insert and after paranthesis if none of the terms and text present3

"""
