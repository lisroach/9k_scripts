#!/usr/bin/env python

############################################################################################################
#		Name: int_brief.py
#		Author: Lisa Roach
#		Date: 8/5/2015
#		Description: The point of this script is to output the ip interface brief command for al the 9k's I have access to
#		Notes: The loops in main() should be adjusted according to the switches you are accessing. The main use of this script is the 
#		show_ip_int_brief function
#
###############################################################################################################

import xmltodict
import json
import sys
from device import Device


def show_ip_int_brief(sw, identity):

	print "\n" +identity + "\n"
	getdata = sw.show('show ip int brief')

	show_int_formated = xmltodict.parse(getdata[1])
	
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

	#The for loops are for looping through the multiple ip addresses of my switches
	#The addresses are not entirely in order, so multiple loops were required


	#change the ranges and ip_appresses to match your switches
	#Change the username and password to match your switches as well.

	for i in range(111, 111):
		ip_address = '111.111.111.' + str(i)
		switch = Device(ip=ip_address, username='username', password='password')
		#open the switch connection
		switch.open()
		#call the  function
		show_ip_int_brief(switch, ip_address)


	for i in range(111, 111):
		ip_address = '###.###.###' + str(i)
		switch = Device(ip=ip_address, username='username', password='password')
		#open the switch connection
		switch.open()

		#call the  function
		show_ip_int_brief(switch, ip_address)

	#This is an example of a sinle ip address not in order. 
	
	ip_address='111.111.111.111'
	switch = Device(ip=ip_address, username='username', password='password')
	switch.open()

	#call the  function
	show_ip_int_brief(switch, ip_address)

if __name__ == "__main__":
	main()
