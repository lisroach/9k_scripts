#!/usr/bin/env python

'''Reads in IP address from a file and outputs the ip interface brief info for each.
 
How to call:
	python int_brief.py <filename>

File:
    The file to be used needs an ip address, username, and password per line in that order. 

Functions:
    show_ip_int_brief - Prints the interface information.
    main - calls the show_ip_int_brief and imports from file


This is a note for the NEWFEATURE feature
'''

import xmltodict
import json
import sys
from device import Device


def show_ip_int_brief(sw, identity):
	'''Output the interface information'''

	try:
		getdata = sw.show('show ip int brief')
		#print out which switch you aer using
		print "\n" +identity + "\n"
		show_int_formated = xmltodict.parse(getdata[1])
	except Exception: #failed to get into switch
		print "There was a problem opening switch:", identity, "Check your username and password."
		sys.exit()

	
	#added KeyError to prevent Errors	
	try:
		#drill down through dictionary
		rows = show_int_formated['ins_api']['outputs']['output']['body']['TABLE_intf']
		row_len = len(rows)

		for i in range(0, row_len): 
			if row_len > 1:
			#From within the dictionary, loop through the nested list to get to the row interfaces
				data = rows[i]['ROW_intf']
			#If there is only one interface it is no longer in a list and needs to be different
			else:
				data=rows['ROW_intf']

			interface= data['intf-name']
			address = data['prefix']
			status = data['proto-state']

			int_dict = {'Interface': interface, 'Ip Address':address, 'Status':status}

			print json.dumps(int_dict, indent=2)
	#end of for loop

	except KeyError: #failed lookup
		print "There was an error with switch " + str(identity)
		#sys.exit() #if there is an error, exit the script

	#passed lookup


def main():
	'''Call the show_ip_int_brief function and read in from file'''
	
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
						#call the  function
						show_ip_int_brief(switch, switch_admin[0])
					else:
						print "Your file variables are incorrect. It should be <ip address> <username> <password> per line."
						sys.exit()
		except IOError:
			print "Your file was mistyped! Please try again."
			sys.exit()

if __name__ == "__main__":
	main()
