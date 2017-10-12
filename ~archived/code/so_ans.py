'''
class Person:

    def __init__(self, fname, sname):
        self.fname = fname
        self.sname = sname
        self.fullname = '{} {}'.format(fname, sname)
        self.email = '{}.{}@email.com'.format(fname, sname)


class Teacher(Person):

    def __init__(self, fname, sname, *subject):
        super().__init__(fname, sname)
        self.subjects = list(subject)

    def add_subject(self, sub):
        self.subjects.append(sub)

    def del_subject(self, sub):
        self.subjects.delete(sub)
	    
    def get_subjects(self):
        return ' '.join(self.subjects)


class Student(Person):

    def __init__(self):
        super().__init__(fname, sname)
        pass

def  dontrun():
	t1 = Teacher('John', 'Becker', 'Maths', 'English')
	print(t1.fullname)
	t1.add_subject(input("Add Subject: "))
	print('Subjects: ')
	for i in t1.subjects:
	    print("=====> ")
	print(t1.get_subjects())
'''

try:
	# do something
except OneTypeOfError as e:
	# handle one type of error one way
	print(e)  # if you want to see the Exception raised but not  raise it
except AnotherTypeOfError as e:
	# handle another type of error another way
	raise e('your own message')
except (ThirdTypeOfError, FourthTypeOfError) as e:
	# handle error types 3 & 4 the same way
	print(e)  # if you want to see the Exception raised but not  raise it
except:  # DONT DO THIS!!!
	'''
	Catches all and any exceptions raised.
	DONT DO THIS. Makes it hard to figure out what goes wrong.
	'''
else:
	# if the try block succeeds and no error is raisedm then do this.
finally:
	'''
	Whether the try block succeeds or fails and one of the except blocks is activated.
	Once all those are done with, finally run this block.
	This works even if your program crashed and so is great for cleaning up for example.
	'''
