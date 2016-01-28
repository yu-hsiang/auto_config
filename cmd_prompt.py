#############################################################
#
#Made by Yu-Hsiang Huang
#Email: yuhsianghh@gmail.com
#
#############################################################

#!/usr/bin/python

import os
import sys
import json
import cmd
import telnetlib

class myprompt(cmd.Cmd):

    prompt = 'my prompt>>'
    def __init__(self, Host, user, password):
        cmd.Cmd.__init__(self)
        self.Host = Host
        self.password = password
        self.user = user
    

    def do_task(self, line):
        '''print out the tasks'''
        key = 0
        title = ""
        content = ""
        D = {}
        i = 1
        
        with open('input.txt', 'r') as input:
            for line in input:
                if line[0] == '%':
                    if not key:
                        key = i
                        title = line
                        i += 1
                    elif content:
                        D.update({key: {'title': title, 'content': content}})
                        key = i
                        i += 1
                        title = line
                        content = ""               
                    else:
                        pass
                elif line[0] == '#':
                    continue
                else:
                    content +=  line
            D.update({key: {'title': title, 'content': content}})
    
        #print "key: ", key
        #print "content:\n", content

        #print json.dumps(D, sort_keys=True, indent = 3, separators=(',', ':'))
        print "***************************************\n"
        print "You have th following procedure: "
        print "***************************************"
        for k in sorted(D.iterkeys()):
                print "(%s)" % k, D[k]['title']
        print "***************************************"

        step = raw_input("Which step you want to do? ")

        try: 
            if int(step) in D:
                print D[int(step)]['title']
                print D[int(step)]['content']
            
                tn = telnetlib.Telnet(self.Host)
                tn.read_until('Username: ')
                tn.write(self.user.encode('ascii') + '\r\n')
                tn.read_until('Password: ')
                tn.write(self.password.encode('ascii') + '\r\n')
                tn.write('enable\n')
                tn.read_until('Password: ')
                tn.write(self.password+'\n\n')
                tn.write(D[int(step)]['content'])
                tn.write('exit\n')
                result = tn.read_all()
                with open('output.txt', 'aw') as output:
                    output.write(result)
                print result
            
            else:
                print "please enter the corect step number!"
        except:
            print "please enter number!"
            
    def do_EOF(self, line):
        '''End of program'''
        return True
        
    

if __name__ == '__main__':
    Host = '10.0.0.1'
    user = 'cisco'
    password = 'cisco'
    mp = myprompt(Host, user, password)
    mp.cmdloop()
