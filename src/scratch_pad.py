import sqlite3


quitter = ''
while quitter == '':
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	
	# Create table
	try:
		c.execute('''CREATE TABLE stocks
		(date text, trans text, symbol text, qty real, price real)''')
	except sqlite3.OperationalError as excep:
		print(excep)
	else:
		# Insert a row of data
		try:
			c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
		except Exception as excep:
			print(excep)
		else:
			print('Done')
	
	# Save (commit) the changes
	conn.commit()
	
	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()
	
	
	
	quitter = input('Continue?')
