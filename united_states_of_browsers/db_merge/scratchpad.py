def incrementer(start=0):
	next = start
	yield next
	while True:
		next += 1
		yield next
		
if __name__ == '__main__':
	inc = incrementer()
	while True:
		print(next(inc))
		input()
