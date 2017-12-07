from pyomegle import OmegleClient,OmegleHandler
import time
import os
import random
import re


chats = 0 
upool = set([0]) 
uhist = {'stranger':[], 'user':[],'collective':[]} 
hist = dict() 
helpt = ''' /h or /help gives 
you these instructions /exit allows 
you to disconnect and quit program 
/next starts a new conversation 
variable names: 
hist[uid][stranger\user\collective] 
'''      
class Hand(OmegleHandler):
    
    def out(self, input_str, verbose=False):
        global chats
        log(self.random_id, 'user', input_str)
        self.send(input_str.strip())
        if verbose:
            print 'timer was at %s'%(time.time()-timer)
        if input_str.strip():
            timer = time.time()
        if verbose:
            print "Timer reset to %s"%(time.time()-timer)
        if verbose:
            print 'Current allowance is %s'%(allowance)
    
    def log(self, pers, text):
        hist[self.random_id][pers].append(text)
        hist[self.random_id]['collective'].append(text)

    def connected(self):
        global upool, hist, uhist, timer
        os.system('clear')
        print 'You\'re now chatting with a random stranger. Say hi!'
        upool.add(self.random_id)
        hist[self.random_id] = uhist
        print 'They\'ve been assigned the username: %s'%(self.random_id)
        timer = time.time()

    def message(self, message):
        global log, chats, timer
        timer = time.time()
        log(self.random_id , 'stranger', message)
        print 'Stranger %s: %s' % (self.random_id , message)
        chats += 1

h = Hand(loop=True) # session loop 
c = OmegleClient(h, wpm=47, lang='en', topics=['politic','political','politics','trump']) 
# 47 words per minute 
c.start() 

verbose = False
while 1:
    allowance = 30 + (chats * 10)
    if (time.time() - timer) >= allowance:
        c.send('Bot timer up you took %s seconds'%(time.time()-timer))
        c.send('you were perscribed only %s due to analysed conversational value'%(allowance)) 
        c.next() 
        chats, timer = 0, time.time()
    else:   
        input_str = raw_input('') # string input
        if input_str.strip() == '/next':
            c.next() 
            chats, timer, time.time(),0
        elif input_str.strip() == '/exit':
            c.disconnect() # disconnect chat session break
            exit() 
        elif input_str.strip() in ['/h','/help']:
            print helpt
        elif input_str.strip() == '/verbose':
            verbose=True
        else:
            out(input_str, verbose)
