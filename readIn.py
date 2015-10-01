'''Read in from File module'''

def read():
#check they entered a filename
	if len(sys.argv) <= 1:
		print "You must enter a filename: int_brief.py <filename>"
		sys.exit()
	
	else:
		#check if the file name is correct and can be opened
		try:
			script, filename = sys.argv
			with open(filename, 'r') as fp:	#with will close file
				for line in fp:				#loop through the lines
					switch_admin = []
					if len(line.split()) == 3:	#check if there are three variables per line

						for word in line.split():	#loop through the words and add them to a list
							#fill a list with the items in the line - should be three
							switch_admin.append(word)
						
						#create the switch object
						switch = Device(ip=switch_admin[0], username=switch_admin[1], password=switch_admin[2])
						switch.open()

					else:
						print "Your file variables are incorrect. It should be <ip address> <username> <password> per line."
						sys.exit()