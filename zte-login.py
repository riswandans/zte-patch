#!/usr/bin/env python
import sys
import telnetlib

host = raw_input("Enter your gateway: ")
user = raw_input("Username: ")
password = raw_input("Password ")

tn = telnetlib.Telnet(host)
tn.read_until("Login: ")
tn.write(user + "\n")

if password:
	tn.read_until("Password: ")
	tn.write(password + "\n")

tn.interact()
print tn.read_all()
