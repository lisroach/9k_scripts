import paramiko
import re
from time import sleep

def bgpcreation(username,password,f):
	### Please Enter the First Switch MGMT IP ###
	#switchIP= raw_input("Please Enter The First Switch MGMT IP: ")
	#Create the shell object
	f.write('[BGP]')
	f.write('\n')
	#Open the file for IP List
	filename= "mgmtIPs.txt"
	with open(filename, 'r') as fp:
		for address in fp:
			address = address.rstrip()
			address = address.replace("'", "")
			if address:
				createtheGoods(address,username,password,f)

def createtheGoods(switchIP,username,password,f):
	ssh= paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		ssh.connect(switchIP, 22, username, password, look_for_keys=False)
	except (paramiko.transport.socket.error,
        paramiko.transport.SSHException,
        paramiko.transport.socket.timeout,
        paramiko.util.log_to_file("filename.log"),
        paramiko.auth_handler.AuthenticationException):
		print 'Error connecting to SSH on %s' % switchIP
	shell = ssh.invoke_shell()
	shell.settimeout(3)
	bgpoutput = getL3(shell, '\nshow ip bgp summ | b Neigh\n')

	peer_ips = []
	test=[]
	for line in bgpoutput.split('\n'):
		#print line
		test= line.split()

	
	non_estab_states = 'neighbor|idle|active|Connect|OpenSent|OpenConfirm'
	for line in bgpoutput.split('\n'):
	    if bool(re.search(non_estab_states, line, re.IGNORECASE)):
	        continue
	    else:
	        ip_regex = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
	        peer_ips.extend(re.findall(ip_regex, line))
	print peer_ips
	for n in peer_ips:
		for line in bgpoutput.split('\n'):
			test= line.split()
			if test[0] == n:
				writetoFile(f,test)
	

def getL3(shell, command):
	shell.send(command.strip() + '\n')
	sleep(3)
 
	output = ''
	while (shell.recv_ready()):
		output += shell.recv(255)
 
	return output

def writetoFile(f,test):
	f.write(test[0]+":"+test[2]+":"+test[8])
	f.write('\n')