#############################################################
#
#Made by Yu-Hsiang Huang
#Email: yuhsianghh@gmail.com
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
import cmd


class TaskPrompt(cmd.Cmd):
    
    prompt = 'TASK PROMPT>'
    
    key = ""
    title = ""
    content = ""
    D = {}
    i = 1
    user = ""
    password = ""
    
    def __init__(self, host, script):
        cmd.Cmd.__init__(self)
        self.host = host
        self.script = script
        
        with open(self.script, 'r') as input:
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
                        title = line
                        self.content = ""               
                    else:
                        pass
                elif line[0] == '#':
                    continue
                else:
                    self.content +=  line
            self.D.update({self.key: {'title': self.title, 'content': self.content}})
        
    def do_task(self, line):
        '''print out the tasks'''
        
        if self.user and self.password:
            print "***************************************\n"
            print "You have th following procedure: "
            print "***************************************"
            for k in sorted(self.D.iterkeys()):
                    print "(%s)" % k, self.D[k]['title']
            print "***************************************"

            step = raw_input("Which step you want to do? ")
         
            if step in self.D:
                print self.D[step]['title']
                print self.D[step]['content']

                try:
                    tn = telnetlib.Telnet(self.host, 23, 2)
                    tn.read_until('Username: ')
                    tn.write(self.user.encode('ascii') + '\r\n')
                    tn.read_until('Password: ')
                    tn.write(self.password.encode('ascii') + '\r\n')
                    tn.write('enable\n')
                    tn.read_until('Password: ')
                    tn.write(self.password+'\n\n')
                    tn.write(self.D[step]['content'])
                    tn.write('exit\n')
                    result = tn.read_all()
                    with open('output.txt', 'aw') as output:
                        output.write(result)
                    print result
                except:
                    print "loggin failed!"
            
            else:
                print "please enter the corect step number!"
        else:
            print "please set your username and password!"
                
            
    def do_user(self, line):
        '''set login user'''
        self.user = line
        print "user name is set to: ", self.user
        
    def do_password(self, line):
        '''set login password'''
        self.password = line
        print "user password is set to: ", self.password
        
    def do_show_user_profile(self, line):
        print "User Name: ", self.user
        print "Password: ", self.password
            
    def do_EOF(self, line):
        '''End of program'''
        return True
    
        
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
        
        if sys.argv[1].endswith(".txt"):
            script = sys.argv[1]
        else:
            print "\n************************************************"
            print "*Please give a text file as the first argument.*"
            print "************************************************\n"
            sys.exit()

    
    TaskPrompt(HOST, script).cmdloop()
