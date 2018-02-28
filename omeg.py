from pyomegle import OmegleClient, OmegleHandler
import time
from threading import Thread
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
        self.pool = []
        self.opener = 'Hello there, what political ideology would you say would best describe your own?'
        self.verbose = False
        self.tout = 30
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
    
    def captcha_required(self):
        """ Called when the server asks for captcha """
        RECAPTCHA_CHALLENGE_URL = 'http://www.google.com/recaptcha/api/challenge?k=%s'
        url = RECAPTCHA_CHALLENGE_URL % challenge
        source = self.browser.open(url).read()
        challenge = recaptcha_challenge_regex.search(source).groups()[0]
        url = RECAPTCHA_IMAGE_URL % challenge

        print ('Recaptcha required: %s' % url)
        response = raw_input('Response: ')

        self.omegle.recaptcha(challenge, response)

    def log(self, pers, text):
        self.hist[self.random_id][pers].append(text)
        self.hist[self.random_id]['collective'].append(pers+': '+text)

    def connected(self):
        os.system('clear')
        self.on = True
        self.chats = 0
        print 'You\'re now chatting with a random stranger. Say hi!'
        while self.random_id in self.upool:
            self.random_id = random.randint(100000, 999999)
        self.upool.add(self.random_id)
        self.hist[self.random_id] = self.uhist
        print 'They\'ve been assigned the username: %s' % (self.random_id)
        
        # Opening message
        ###################
        self.out(self.opener)
        self.pool = Thread(target=self.timer)
        self.pool.start()

    def message(self, message):
        self.time = time.time()
        self.log('stranger', message)
        print '\nStranger %s: %s' % (self.random_id, message)
        self.chats += 1
        self.analyze(message)
        
    def analyze(self, message):
        if '*their' in message or "they're" in message:
            self.out('*Notice* Warning you have been flagged for pedantry')
            self.out("Pedantry is a sign of intellectual insecurity") 
            self.out("Your attempt to discredit someone through non-relevant attention to detail (probably classist based) only reveals your insecurities about your capacity to think critically and focus on the content") 

    def timer(self):
        if self.verbose:
            print('Service: timer started\n')
        t = time.time()
        while self.chats == 0:
           if self.chats >= 1:
               break
           elif int(time.time()) - int(t) >= self.tout:
               self.out("*Notice* you took too long to reply you have timed out")
               self.client.next()
               self.chats = 0
               break
        if self.verbose:
            print('Service: evade disengaged\n')

def xin(inp):
    val, rec = '', False
    for char in inp:
        if rec:
            val += char
        elif char == ' ':
            rec = True
    return val

h = Hand(loop=True)  # session loop
c = OmegleClient(h, wpm=47, lang='en', topics=[
                 'politic', 'political', 'politics', 'trump'])
# 47 words per minute
c.start()
h.client(c)
timeout = 0.1  # seconds
verbose = False
while 1:
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
        print h.helpt
    elif input_str.strip() in ['\\timer', '\\t']:
        h.tout = int(''.join([x for x in input_str.strip() if x.isdigit()]))
    elif input_str.strip() in ['\\verbose', '\\v']:
        h.verbose = True
    elif input_str.strip() in ['\\opener', '\\o']:
        h.opener = xin(input_str.strip())
    elif input_str.strip() in ['\\spam']:
        for _ in range(10):
            h.out(xin(input_str.strip()), verbose)
    else:
        if h.on == True:
            h.out(input_str, verbose)
