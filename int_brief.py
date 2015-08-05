#!/usr/bin/env python
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

	#need to pull the switch data

	for i in range(133, 139):
		ip_address = '172.31.217.' + str(i)
		switch = Device(ip=ip_address, username='admin', password='cisco123')
		#open the switch connection
		switch.open()
		#call the  function
		show_ip_int_brief(switch, ip_address)


	for i in range(142, 145):
		ip_address = '172.31.217.' + str(i)
		switch = Device(ip=ip_address, username='admin', password='cisco123')
		#open the switch connection
		switch.open()

		#call the  function
		show_ip_int_brief(switch, ip_address)

		#changed from 149
	ip_address='172.31.217.149'
	switch = Device(ip=ip_address, username='admin', password='cisco123')
	switch.open()

	#call the  function
	show_ip_int_brief(switch, ip_address)

if __name__ == "__main__":
	main()