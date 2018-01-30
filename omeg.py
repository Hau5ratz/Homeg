from pyomegle import OmegleClient, OmegleHandler
import time
from multiprocessing.dummy import Pool as ThreadPool 
import os
import random
import sys
import select
import pickle
import os

class Hand(OmegleHandler):
    def __init__(self, *args, **kwargs):
        OmegleHandler.__init__(self, *args, **kwargs)
        if not os.path.isdir('./data'):
            os.mkdir('./data')   
        if not os.path.isfile('./data/chats'):
            self.hist = dict()
        else:
            with open('chats', 'rb') as handle:
                self.hist = pickle.load(handle)
        self.uhist = {'stranger': [], 'user': [], 'collective': []}
        self.upool = set([0])
        self.random_id = 0
        while self.random_id in self.upool:
            self.random_id = random.randint(100000, 999999)
        self.chats = 0
        self.pool = ThreadPool(1) 
        self.tout = 15
        self.on = False
        self.hist = dict()
        self.helpt = ''' /h or /help gives
                     you these instructions /exit allows
                     you to disconnect and quit program
                     /next starts a new conversation
                     variable names:
                     hist[uid][stranger\user\collective]
                     '''

    def out(self, input_str, verbose=False):
        self.log('user', input_str)
        self.client.send(input_str.strip())
        if verbose:
            pass  # print 'timer was at %s' % (time.time() - timer)
        if input_str.strip():
            pass  # timer = time.time()
        if verbose:
            pass  # print "Timer reset to %s" % (time.time() - timer)
        if verbose:
            pass
        
    def client(self, c):
        self.client = c

    def log(self, pers, text):
        self.hist[self.random_id][pers].append(text)
        self.hist[self.random_id]['collective'].append(text)

    def connected(self):
        os.system('clear')
        self.on = True
        print 'You\'re now chatting with a random stranger. Say hi!'
        while self.random_id in self.upool:
            self.random_id = random.randint(100000, 999999)
        self.upool.add(self.random_id)
        self.hist[self.random_id] = self.uhist
        print 'They\'ve been assigned the username: %s' % (self.random_id)
        
        # Opening message
        ###################
        self.out('Mod: Hey what political ideology would you say you identify with?')
        self.pool.map(self.timer, [self.tout])
        self.pool.close

    def message(self, message):
        self.timer = time.time()
        self.log('stranger', message)
        print '\nStranger %s: %s' % (self.random_id, message)
        self.chats += 1

    def timer(self, tout):
        t = time.time()
        while not self.hist[self.random_id]['stranger']:
           if int(time.time()) - int(t) >= tout:
               self.out("Mod: *Notice* you have timed out stop wasting people's time")
               self.client.next()
               
     
print 'loading objects'
h = Hand(loop=True)  # session loop
c = OmegleClient(h, wpm=47, lang='en', topics=[
                 'politic', 'political', 'politics', 'trump'])
# 47 words per minute
print 'initializing objects'
c.start()
h.client(c)
print 'running program'
read_list = [sys.stdin]
timeout = 0.1  # seconds
verbose = False
print 'before loop'
while 1:
    print 'at raw'
    input_str = raw_input()
    if input_str.strip() == '\\next':
        h.on = False
        c.next()
    elif input_str.strip() == '\\exit':
        with open('chats', 'wb') as handle:
            pickle.dump(h.hist, handle)
        c.disconnect()  # disconnect chat session break
        exit()
    elif input_str.strip() in ['\\h', '\\help']:
        print helpt
    elif '\\t' in input_str.strip():
        h.tout = int(''.join([x for x in input_str.strip() if x.isdigit()]))
    elif input_str.strip() == '\\verbose':
        verbose = True
    else:
        if h.on == True:
            h.out(input_str, verbose)
