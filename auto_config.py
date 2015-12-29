#############################################################
#
#Made by Yu-Hsiang Huang
#
#############################################################

#!/usr/bin/python

import getpass
import sys
import telnetlib
import os
import re
import socket
import json


class automation(object):

    key = 0
    title = ""
    content = ""
    D = {}
    i = 1
    
    def __init__(self, host, user, password, script):
        self.host = host
        self.user = user
        self.password = password
        self.script = script
    
    def interact(self, tn):
        print "***************************************\n"
        print "You have th following procedure: "
        print "***************************************"
        for k in sorted(self.D.iterkeys()):
                print "(%s)" % k, self.D[k]['title']
        print "***************************************"
    
        q1 = raw_input("whcih step are you ready to go on? or enter \'No\' to stop: ")
    
        if q1 in self.D:
            q2 = raw_input("Are you ready to go?(yes/no)")
            if q2.lower() == "y" or q2.lower() == "yes":
                print self.D[q1]['title']
                print self.D[q1]['content']
                tn.write(self.D[q1]['content'])
                output = tn.read_until(b"end\n").encode('ascii')
                print "OUTPUT\n", output
                
                self.interact(tn)
            elif q2.lower() == "n" or q2.lower() == "no":
                self.interact(tn)
            else:
                print "Please enter yes or no to continue."
                self.interact(tn)
        elif q1.lower() == 'n' or q1.lower() == 'no':
            pass
        else:
            print "************************************\n"
            print "Please enter the corect step number!\n\n\n\n"
            print "************************************\n"
            self.interact(tn)
           
        
    def load_script(self):
        
        try:
            with open('input.txt', 'r') as input:
                for line in input:
                    if line[0] == '%':
                        if not self.key:
                            self.key = str(self.i)
                            self.title = line
                            self.i += 1
                        elif self.content:
                            self.D.update({self.key: {'title': self.title, 'content': self.content}})
                            self.key = str(self.i)
                            self.i += 1
                            self.title = ""
                            self.content = []                
                        else:
                            pass
                    elif line[0] == '#':
                        continue
                    else:
                        self.content += line
                self.D.update({self.key: {'title': self.title, 'content': self.content}})
                print "Script has been loaded successfully!"
        except IOError:
            print "failed to load your file!"
            sys.exit()
    
    def telnet(self):

        try:
            tn = telnetlib.Telnet(self.host, 23, 5)
            tn.set_debuglevel(5)
        except IOError:
            print "destination unreachable!"
            sys.exit()
    
        try:
            tn.read_until(b"Username: ", 3)
            tn.write(self.user.encode('ascii') + b"\r\n")
            if self.password:
                tn.read_until(b"Password: ", 3)
                tn.write(self.password.encode('ascii') + b"\r\n")
        except IOError:
            print "Login failed!"
            tn.close()
            sys.exit()  
        
        try:
            if "Login invalid" in tn.read_some():
                tn.close()
                sys.exit()
            else:
                self.interact(tn)
            
        except IOError:
            print "nothing happend!"
            tn.close()
            sys.exit()
        

        
if __name__ == "__main__":
    
    
    p = re.compile("^([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\." \
                    "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\."\
                    "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\."\
                    "([1-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-4])$")
    
    if len(sys.argv) < 3:
        print "\n***********************\n*You need 2 arguments!*\n***********************\n"
        sys.exit()
    else:
        
        if p.match(sys.argv[2]):
            HOST = sys.argv[2]
        else:
            print "\n********************************************\n"
            print "*Ths second argument is not a host address!*"
            print "\n********************************************\n"
            sys.exit()
        
        '''
        try:
            socket.inet_aton(sys.argv[2])
            HOST = sys.argv[2]
        except IOError:
            print "\n********************************************\n"
            print "*Ths second argument is not a host address!*"
            print "\n********************************************\n"
            sys.exit()
        '''
        
        if sys.argv[1].endswith(".txt"):
            script = sys.argv[1]
        else:
            print "\n************************************************"
            print "*Please give a text file as the first argument.*"
            print "************************************************\n"
            sys.exit()

    
    user = raw_input("Enter your remote account: ")
    password = getpass.getpass(prompt = "Enter your password: ")
    
    my_auto = automation(HOST, user, password, script)
    my_auto.load_script()
    my_auto.telnet()

    

