  
	orchestrator.OrchestratorObj.find_installed_browsers(): Finds the browsers installed by checking the existing of the the default paths.  
	orchestrator.OrchestratorObj.make_records_yielders(): Creates instances of the Browser class, one instance for each Browser discovered.  

	browser.BrowserObj.__init__():
		
		Calls BrowserObj.make_paths()
			creates browserpaths.BrowserPaths object
				BrowserPaths, upon _init__ reads browser_data.py and uses it to 
				construct the necessary paths to the sqlite files for the each browser.
				Returns the paths to Browser_obj.
		Calls Browser_obj.add_tables_for_access({filename: tablename})
			creates and calls Table_obj from table.Table
				Each table is for a specific table from a specific sqlite file.
				The dict of {tablename: Table_obj} is stored in Browser_obj.tables
					
					Iterates and calls each stored Table_obj's make_records_yielder(),
					which yields the yielder for each table
					in Table_obj.records_yielder
				
					
		Calls browser_obj.access_fields({tablename: fieldname})
			which uses Table_obj record_yielder to generate each record 
			and only keeps the fields specified for their respective table.
			Yields that record, (hence is a generator of records).
	
	orchestrator.DatabaseMergeOrchestrator:
		then collects all the browser.record_yielders and passes it on one at a time to
		orchestrator.write_records()

