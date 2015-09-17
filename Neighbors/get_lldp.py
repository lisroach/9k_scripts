#!/usr/bin/env python

'''

Get the device relationships and add them to a file

Filename: neighbors.txt (file will be rewritten everytime script runs)
File format: <hostname_current> <current_port> <hostname_neighbor> <neighbors_port>

Author: Lisa Roach
Date of last revision: 9/16/2015

'''

import xmltodict
import json
import sys
from device import Device


def show_lldp_neigh(sw, identity, f, ip):
	'''Add lldp neighbors information to file'''

	print "I made it here"

	try:
		getdata = sw.show('show lldp neighbors')		
		
		formatted_data = xmltodict.parse(getdata[1])
		
		rows = formatted_data['ins_api']['outputs']['output']['body']['TABLE_nbor']['ROW_nbor']

		f.write('\n[Switch: ' + str(identity) + ' | MgmtIP: '+ ip + '] \n' + '[LLDP] \n')
		for i in range(0, len(rows)):					
			f.write(rows[i]['l_port_id'] + ':')
			f.write(rows[i]['chassis_id'] + ':')
			f.write(rows[i]['port_id'] + '  \n')		
	#end of for loop 

	except KeyError: #failed lookup
		print "There was an error with switch " + identity
		#sys.exit() #if there is an error, exit the script

def get_switch(ip_address, username, password, f):
	'''Open the switch, grab the hostname, and run show_lldp_neigh'''

	try:
		switch = Device(ip=ip_address, username=username, password=password)
		switch.open()	

		print ip_address

		xmlHostname = switch.show('show hostname')
		dictHostname = xmltodict.parse(xmlHostname[1])		
		hostname = dictHostname['ins_api']['outputs']['output']['body']['hostname']

		show_lldp_neigh(switch, hostname, f, ip_address)	
		

	except Exception: #failed lookup
		pass

	


