from collections import namedtuple

from united_states_of_browsers.oops import Table

TableData = namedtuple('TableData','table, path, browser, file, profile')

firefox_profile_path = 'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\'
chrome_profile_path = 'C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\'
init_testdata_input = (
	TableData(table='moz_places',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	TableData(table='moz_bookmarks',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	TableData(table='moz_places',
	          path=firefox_profile_path+'udd5sttq.test_profile2\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile2',
	          ),
	TableData(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	TableData(table='urls',
	          path=chrome_profile_path+'Profile 1\\History',
	          browser='chrome',
	          file='history',
	          profile='Profile 1',
	          ),
	)

init_testdata_expected = [
	Table(table='moz_places',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	Table(table='moz_bookmarks',
	          path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile1',
	          ),
	Table(table='moz_places',
	          path=firefox_profile_path+'udd5sttq.test_profile2\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='test_profile2',
	          ),
	Table(table='moz_places',
	          path=firefox_profile_path+'r057a01e.default\\places.sqlite',
	          browser='firefox',
	          file='places.sqlite',
	          profile='default',
	          ),
	Table(table='urls',
	          path=chrome_profile_path+'Profile 1\\History',
	          browser='chrome',
	          file='history',
	          profile='Profile 1',
	          ),
	]

make_records_testdata_input = [
	Table(table='moz_places',
		path=firefox_profile_path+'kceyj748.test_profile1\\places.sqlite',
		browser='firefox',
		file='places.sqlite',
		profile='test_profile1',
		),
	Table(table='urls',
		path=chrome_profile_path+'Profile 1\\History',
		browser='chrome',
		file='history',
		profile='Profile 1',
		),
	]
make_records_testdata_expected = (
	set(['place:sort=8&maxResults=10',
	'place:type=6&sort=14&maxResults=10',
	'https://www.mozilla.org/privacy/firefox/',
	'https://www.nytimes.com/2017/10/20/opinion/sunday/to-complain-is-to-truly-be-alive.html',
	'https://www.wired.com/story/google-sidewalk-labs-toronto-quayside/',
	'https://www.outsideonline.com/2243621/appalachian-hustle',
	'place:type=3&sort=4',
	'place:transition=7&sort=4',
	'place:type=6&sort=1',
	'place:folder=TOOLBAR',
	'place:folder=BOOKMARKS_MENU',
	'place:folder=UNFILED_BOOKMARKS',
	    ]),
	set(['https://www.google.com/search?q=test&oq=test&aqs=chrome..69i57j0l5.789j0j7&sourceid=chrome&ie=UTF-8',
	'http://www.gmail.com/',
	'https://www.gmail.com/',
	'https://www.google.com/gmail/',
	'https://mail.google.com/mail/',
	'https://accounts.google.com/ServiceLogin?service=mail&passive=true&rm=false&continue=https://mail.google.com/mail/&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1#',
	'https://mail.google.com/intl/en/mail/help/about.html#',
	'https://www.google.com/intl/en/mail/help/about.html#',
	'https://www.google.com/gmail/about/#',
	'https://www.google.com/search?q=village+dental+nyc&oq=village+dental+nyc&aqs=chrome..69i57j0l5.2878j0j7&sourceid=chrome&ie=UTF-8',
	'http://www.villagedentalnyc.com/',
	'https://www.ident.ws/template_include/new_patient_sign_in.do?site=10679&practiceId=37810',
	'https://www.ident.ws/template_include/new_patient_forms.do?FirstName=Kshitij&MI=&LastName=Chawla&apptDate=12%2F12%2F2017',
	'https://www.ident.ws/template_include/questionnaire_form.do?id=2785850972',
	'http://www.yahoo.com/',
	'https://www.yahoo.com/',
	'https://www.ident.ws/template_include/cal.jsp?format=MM%2FDD%2FYYYY&datefield=document.forms.signInForm.apptDate',
	'https://coderpad.io/ZARYRHRP',
	'https://mail.google.com/mail/u/0/#inbox',
	'https://accounts.google.com/AccountChooser?service=mail&continue=https://mail.google.com/mail/',
	'https://accounts.google.com/ServiceLogin?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1',
	'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin',
	    ]),
	)

def additional_tests_drafts():
	def test_table():
		table = Table('1', '2', '3', '4', '5')
	
	def test_firefox():
		table2 = Table(table='moz_places',
		               path=Path(
			               'C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\px2kvmlk.RegularSurfing_glitch\\places.sqlite'),
		               browser='firefox',
		               file='places.sqlite',
		               profile='RegularSurfing',
		               )
		table2.get_records()
		# for record_yielder in table2.records_yielder:
		# 	pass
		# print(dict(record_yielder))
		
		table3 = Table(table='moz_places',
		               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\e0pj4lec.test_profile0\\places.sqlite',
		               browser='firefox',
		               file='places.sqlite',
		               profile='test_profile0',
		               )
		table3.get_records()
		for record_yielder in table3.records_yielder:
			pass
		# print(dict(record_yielder))
		
		table4 = Table(table='moz_places',
		               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
		               browser='firefox',
		               file='places.sqlite',
		               profile='test_profile0',
		               )
		# table4.get_records()
		# for record_yielder in table4.records_yielder:
		# 	pass
		# 	print(dict(record_yielder))
		
		table5 = Table(table='moz_places',
		               path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\kceyj748.test_profile1\\places.sqlite',
		               browser='firefox',
		               file='places.sqlite',
		               profile='test_profile0',
		               )
		table5.get_records()
		for record_yielder in table5.records_yielder:
			pass
	
	# print(dict(record_yielder)['url'])
	
	def test_chrome():
		table2 = Table(table='urls',
		               path='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\history',
		               browser='chrome',
		               file='history',
		               profile='Default',
		               )
		not_null_fieldnames = define_non_null_fields(table2)
		
		table2.get_records()
		for record_yielder in table2.records_yielder:
			print(dict(record_yielder))
	
	def test_define_non_null_fields():
		table_fx = Table(table='moz_places',
		                 path='C:\\Users\\kshit\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\udd5sttq.test_profile2\\places.sqlite',
		                 browser='firefox',
		                 file='places.sqlite',
		                 profile='test_profile0',
		                 )
		not_null_fieldnames = define_non_null_fields(table_fx)
		print(not_null_fieldnames, table_fx['non_null_fields'], table_fx.non_null_fields)
		table_cr = Table(table='urls',
		                 path='C:\\Users\\kshit\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\history',
		                 browser='chrome',
		                 file='history',
		                 profile='Default',
		                 )
		not_null_fieldnames = define_non_null_fields(table_cr)
		print(not_null_fieldnames, table_cr['non_null_fields'], table_cr.non_null_fields)
	
	def print_table_attr(obj):
		attrs = ('table', 'path', 'browser', 'file', 'profile')
		print([obj[attr_] for attr_ in attrs])
		print(obj)
		print('__str__:', repr(obj))
		print('__repr__:', obj.table)
	
	def test():
		test_table()
		test_firefox()
		test_chrome()
		test_define_non_null_fields()
