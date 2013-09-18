#!/usr/bin/env python

from mailclient import MailClient
from socket import *
import sys

try:
    fromEmail  = sys.argv[1]
    toEmail    = sys.argv[2]
except:
    raise SystemExit("Usage: mailclient.py <From Email> <To Email>")

smtpPort   = 25

clientSocket = socket(AF_INET, SOCK_STREAM)

MC = MailClient(clientSocket, fromEmail, toEmail)

if MC.emailvalidation(toEmail) and MC.emailvalidation(fromEmail):
    MC.getinput()
    MC.send()
    print "Message Successfully sent to %s" %toEmail
else:
	raise SystemExit("Invalid email address")

clientSocket.close()