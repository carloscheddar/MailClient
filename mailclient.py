#!/usr/bin/env python
#
# Author: Carlos Feliciano Barba
# Email: c.feliciano2009@gmail.com
# GitHub: carloscheddar
#
#Simple SMTP client using sockets.
#Dependencies: dnspython -- pip install dnspython

from socket import *
import re

#import dns.resolver to get the MX server names.
try:
    import dns.resolver
except ImportError:
    raise SystemExit("Please install dnspython using: pip install dnspython")


class MailClient():
    def __init__(self, socket, fromEmail, toEmail):
        self.fromEmail = fromEmail
        self.toEmail = toEmail
        self.socket = socket

    def receive(self):
        #Print verbose messages if the user imputs 'v'.
        self.socket.recv(1024)

    def getinput(self):
        self.subject = raw_input("Enter Subject: ")
        self.message = raw_input("Enter Message: ")

    def getmailserver(self):
        #Split email to get the domain name
        domain = self.toEmail.split('@')[1]

        #Use domain to get the proper MX server
        #split the string until only the mx server is left.
        self.mailServer = dns.resolver.query(domain, 'MX')[0].to_text().split(' ')[1]

    #Function to validate email
    def emailvalidation(self, email):
        email_pattern = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
        if re.match(email_pattern, email) == None:
            print email
            return False
        else:
            return True


    #Function that sends and receives according to smtp protocol
    #For each message sent there is a response.
    def send(self):
        self.getmailserver()
        self.socket.connect((self.mailServer, 25))
        self.receive()
        self.socket.send("helo\r\n") #Be classy and say hello.
        self.receive()
        self.socket.send("mail from:<%s>\r\n"     % self.fromEmail)
        self.receive()
        self.socket.send("rcpt to:<%s>\r\n"       % self.toEmail)
        self.receive()
        self.socket.send("data\r\n")
        self.receive()
        self.socket.send("From: <%s>\r\n"         %self.fromEmail
                          +"To: <%s>\r\n"         %self.toEmail
                          +"Subject: %s\r\n\r\n"  %self.subject
                          +"%s\r\n"               %self.message
                          +"\r\n.\r\n")
        self.receive()
        self.socket.send("quit\r\n")
        self.receive()

