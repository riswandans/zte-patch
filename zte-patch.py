#!/usr/bin/env python
import sys
import telnetlib

def print_warning(str):
	print '\033[93m' + str + '\033[0m'

def print_success(str):
	print '\033[92m' + str + '\033[0m'
	
def vulnerable_test(host):
	user = "root"
	password = "Zte521"

	tn = telnetlib.Telnet(host)
	tn.read_until("Login: ")
	tn.write(user + "\n")

	if password:
    		tn.read_until("Password: ")
    		tn.write(password + "\n")

	tn.write("ls\n")
	tn.write("exit\n")
	return tn.read_all()
	tn.close()

def vulnerable_patch(host, new_user, new_password):
	user = "root"
	password = "Zte521"

	tn = telnetlib.Telnet(host)
	tn.read_until("Login: ")
	tn.write(user + "\n")

	if password:
    		tn.read_until("Password: ")
    		tn.write(password + "\n")

	if new_user != user:
		tn.write("sendcmd 1 DB set TelnetCfg 0 TS_UName " + new_user + "\n")

	if new_password != password:
		tn.write("sendcmd 1 DB set TelnetCfg 0 TS_UPwd " + new_password + "\n")
	
	tn.write("sendcmd 1 DB save\n")
	tn.write("exit\n")
	return tn.read_all()
	tn.close()

print "-------------- ZTE Patch --------------"
print "[-] ZTE F609"
print "[-] ZTE F620"
print "[-] ZTE F640"
print "[-] ZTE F660"
print "----------------------------------------"

host = raw_input("Enter your IP Gateway: ")
check = vulnerable_test(host)
if check.find('Busy') >= 0:
	print_warning("[!] Your gateway is vulnerable")
else:
	print_success("[*] Your gateway not vulnerable")
	sys.exit()

valid_user = raw_input(">> Change default root username? (y/n) ")
if valid_user == "y":
	username = raw_input("New username: ")
else:
	username = "root"

valid_user = raw_input(">> Change default password for " + username + "? (y/n) ")
if valid_user == "y":
	password_1 = raw_input("New password: ")
	confirm_password = raw_input("Confirm new password: ")
	if password_1 == confirm_password:
		password = password_1
	else:
		print "Incorrect password"
else:
	password = "Zte521"

patch = vulnerable_patch(host, username, password)
if patch.find('Denied') >= 0:
	print_warning("[!] Failed to execute commands, Access Denied")
else:
	if username != "root" and password != "Zte521":
		print_success("[*] Success patch your router")
	else:
		print_warning("[!] Failed patch, setting have not changed")
	print "Username " + username
	print "Password " + password
	print "Reboot your modem/router"
