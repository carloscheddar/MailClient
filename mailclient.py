#!/usr/bin/env python
#
# Author: Carlos Feliciano Barba
# Email: c.feliciano2009@gmail.com
# GitHub: carloscheddar
#
#Simple SMTP client using sockets.
#Dependencies: dnspython -- pip install dnspython

from socket import *
import sys, dns.resolver

smtpPort   = 25
try:
    fromEmail  = sys.argv[1]
    toEmail    = sys.argv[2]
except:
    raise SystemExit("Usage: mailclient.py <From Email> <To Email>")

#Split email to get the domain name
domain = toEmail.split('@')[1]

#Use domain to get the proper MX server
mailServer = dns.resolver.query(domain, 'MX')[0].to_text().split(' ')[1]


class MailClient():
    def __init__(self, socket):
        self.socket = socket

    def receive(self):
        #Print verbose messages if the user wants to.
        try:
            sys.argv[3] == 'v'
            print self.socket.recv(1024)
        except IndexError:
            self.socket.recv(1024)

    def getinput(self):
        subject = raw_input("Enter Subject: ")
        message = raw_input("Enter Message: ")
        return subject, message


    #Function that sends and receives according to smtp protocol
    def send(self):
        self.receive()
        self.socket.send("helo\n") #Be classy and say hello.
        self.receive()
        self.socket.send("mail from:<%s>\n"     % fromEmail)
        self.receive()
        self.socket.send("rcpt to:<%s>\n"       % toEmail)
        self.receive()
        self.socket.send("data\n")
        self.receive()
        self.socket.send("From: <%s>\n"         %fromEmail
                          +"To: <%s>\n"         %toEmail
                          +"Subject: %s\n\n"    %subject
                          +"%s\n"               %message
                          +"\r\n.\r\n")
        self.receive()
        self.socket.send("quit\n")
        self.receive()

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((mailServer, smtpPort))

MC = MailClient(clientSocket)
subject, message = MC.getinput()
MC.send()

clientSocket.close()
