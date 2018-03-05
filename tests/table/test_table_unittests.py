from pprint import pprint

from united_states_of_browsers.db_merge.table import Table
from tests.table import test_table_setup as tts

class TestTable:
	@classmethod
	def test_exception_no_such_table(self):
		test_cases = tts.no_such_table_test_setup()
		for test in test_cases:
			table_obj = Table(*test)
			exception_raised = table_obj.get_records()
			# table_obj.records_yielder.fetchone()
			for record in table_obj.records_yielder:
				print(record)
			print(exception_raised)
		

TestTable.test_exception_no_such_table()



#
# info = tts.no_such_table_test_setup()
# print(tuple(info)[0])

