#!/usr/bin/env python

import get_lldp
import sys
import getpass
import l3_scrape


def main():
	
	username = raw_input("Username: ")
	password = getpass.getpass("Password: ")

	try:
		read_file = "mgmtIPs.txt"
		working_file = open('neighbors.txt', 'w')
		with open(read_file, 'r') as fp:	#with will close file
			for address in fp:
				address = address.rstrip()
				address = address.replace("'", "")
				#if address:
					#get_lldp.get_switch(str(address), username, password, working_file)

		l3_scrape.bgpcreation(username, password, working_file)

					

		print "\nScript complete! Check the 'neighbors.txt' file that has been generated.\n"
		working_file.close()


	except IOError:
		print "There is something wrong with your management IP file"

	
if __name__ == "__main__":
	main()