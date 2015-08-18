#!/usr/bin/env python

"Darius Carrier / dacarrie@cisco.com"

'''
The goal of this script is to monitor the "up" interfaces on switches that you choose
and notify the administrator, through email, when one of those interfaces goes down

How to call:
python Monitor_Interfaces <list_switches> <email_info>

File Formats:

<list_switches> should include the hostname and ip address of the switches. Ex:
N9K1 1.1.1.1
N9K2 2.2.2.2

<email_info> should include email address and password (This should be changed in the future)
email@email.com password

Side Notes (How to use):
You will first be prompted with the list of switches and IP addresses that you provided
in the text file. Please enter each switch you would like to monitor seperated by commas
for example:
	N9K1,N9K2,N9K3
'''

import xmltodict
import json
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from device import Device


def getswitchinfo(sw):
	switch = Device(ip=sw)
	switch.open()
	getdata = switch.show('show interface brief')

	show_intf_dict = xmltodict.parse(getdata[1])

	data = show_intf_dict['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']

	#rint data
	# Code to loop through interfaces and put all 'up' in a list (align list with key)
	up_list= []
	for each in data:
		if 'up' in each.values():
			up_list.append(each['interface'])
	#print up_list
	return up_list

	############################################################

def firstloop(user_list,first_loop,list_switches,monitor):
	while first_loop:
		for i in user_list:
			up_list =getswitchinfo(list_switches[i])
			if i not in monitor:
				monitor[i]= up_list
			else:
				"do nothing"
		return monitor
		first_loop= False

def maintain_interfaces(list_switches,monitor,email_info):
	for i in monitor:
		check_list= getswitchinfo(list_switches[i])
		print monitor[i]
		for x in monitor[i]:
			match= False
			for y in check_list:
				if x==y:
					check_list.remove(y)
					match= True
			if match != True:
				### Send the email and pop that item from monitor
				print "Interface Down"
				send_email(x,email_info)
				monitor[i].remove(x)
				
		#Add an interface that just came up
		if check_list:
			for y in check_list:
				monitor[i].append(y)

def send_email(x,email_info):
	for key,value in email_info.iteritems():
		email_address= key
		password = value
	fromaddr = email_address
	toaddr = email_address
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Interface "+x+" Went Down"
	 
	body = "Dude something went wrong, interface "+x+" is down"
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP('mail.cisco.com', 587)
	server.starttls()
	server.login(fromaddr, password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


def main():

	monitor = {}
	list_switches = {}
	email_info = {}

	#check they entered a filename
	if len(sys.argv) <= 2:
		print "You must enter a filename: int_brief.py <filename>"
		sys.exit()
	
	else:
		#check if the file name is correct and can be opened
		try:
			script, filename, filename2 = sys.argv
			with open(filename, 'r') as fp:	#with will close file
				for line in fp:				#loop through the lines
					if len(line.split()) == 2:	#check if there are two variables per line
						words= line.split()
						list_switches[words[0]]= words[1]
					else:
						print "Your file variables are incorrect. It should be <hostname> <ip address>"
						sys.exit()
			with open(filename2, 'r') as fp2:
				for line in fp2:
					if len(line.split()) == 2:	#check if there are two variables per line
						words= line.split()
						email_info[words[0]]= words[1]
					else:
						print "Your file variables are incorrect. It should be <email> <password>"
						sys.exit()
		except IOError:
			print "Your file was mistyped! Please try again."
			sys.exit()
	print ''
	print "Please Choose switch(es) to monitor (Separated by commas)"
	print "==================================="
	for key,value in list_switches.iteritems():
		print key, value

	switches= raw_input()
	user_list= switches.split(",")

	for i in user_list:
		if i in list_switches:
			"do nothing"
		else:
			print "Error Switch Does Not Exist. Exiting......"
			break

	first_loop= True
	monitor= firstloop(user_list,first_loop,list_switches,monitor)
	while 1:
		maintain_interfaces(list_switches,monitor,email_info)
	
	


if __name__ == "__main__":
	main()