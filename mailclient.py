#!/usr/bin/env python
#
# Author: Carlos Feliciano Barba
# Email: c.feliciano2009@gmail.com
# GitHub: carloscheddar
#
#Simple SMTP client using sockets.

from socket import *
import sys

mailServer = "gmail-smtp-in.l.google.com"
smtpPort   = 25
try:
    fromEmail  = sys.argv[1]
    toEmail    = sys.argv[2]
except:
    raise SystemExit("Usage: mailclient.py <From Email> <To Email>")


class MailClient():
    def __init__(self, socket):
        self.socket = socket

    def receive(self):
        self.socket.recv(1024)

    def getinput(self):
        subject = raw_input("Enter Subject: ")
        message = raw_input("Enter Message: ")
        return subject, message


    #Function that sends and receives according to smtp
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
