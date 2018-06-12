from pyomegle import OmegleClient, OmegleHandler
import time
from threading import Thread
import os
import requests
import random
import sys
import select
import pickle

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
        self.looking = False
        while self.random_id in self.upool:
            self.random_id = random.randint(100000, 999999)
        self.chats = 0
        self.pool = []
        self.opener = 'Hello there, what political ideology would you say would best describe your own?'
        self.verbose = False
        self.tout = 20
        self.on = False
        self.app_id = 'fb993127'
        self.app_key = 'ff75e31b321674eb786dd2b2619617ab'
        self.hist = dict()
        self.helpt = ''' /h or /help gives
                     you these instructions /exit allows
                     you to disconnect and quit program
                     /next starts a new conversation
                     variable names:
                     hist[uid][stranger\\user\\collective]
                     '''
        
        
        self.d = '''Source: %s
                      Word: %s
                      definition: %s
                   '''
        self.c = '''A communist society is characterized by common ownership of the means of production with free access to the articles of consumption and is classless and stateless, implying the end of the exploitation of labour (source: https://en.wikipedia.org/wiki/Communist_society).
        There is a frequent mis-characterization of countries that appropriate the name of socialism and communism to mascarade as non-facist countries.
        Both German and Italian facists are literally on record as acknowleding state capitalist regiemes (USSR, MAOIST china) as forms of facism (source: https://en.wikipedia.org/wiki/Red_facism). Litterally both the left and right wing are in agreement that there has never been a truely communist country.
        It's just you, literally just you are retarded enough to buy into that bullshit idea because you litterally have no idea what you're talking about.''' 
        
    def waiting(self):
        """ Called when we are waiting for a stranger to connect """
        print ('Looking for someone you can chat with...')
        self.looking = True
        
    def _setup(self, omegle):
        """ Called by the Omegle class for initial additional settings """
        self.omegle = omegle
        self.omegle.browser.set_proxies({"http": "101.128.73.201:8080"})
        self.omegle.browser.set_handle_robots(False)

    def connected(self):
        """ Called when we are connected with a stranger """
        print ('You\'re now chatting with a random stranger. Say hi!')
        self.looking = False

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
        print('Captcha Challenge work in progress')
        exit()
        '''
        global challenge
        RECAPTCHA_CHALLENGE_URL = 'http://www.google.com/recaptcha/api/challenge?k=%s'
        url = RECAPTCHA_CHALLENGE_URL % challenge
        source = self.browser.open(url).read()
        challenge = recaptcha_challenge_regex.search(source).groups()[0]
        url = RECAPTCHA_IMAGE_URL % challenge

        print ('Recaptcha required: %s' % url)
        response = raw_input('Response: ')

        self.omegle.recaptcha(challenge, response)
        '''

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
        
    def define(self, word):
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/%s'
        header = {'app_id': self.app_id, 'app_key': self.app_key}
        r = requests.get(url%word.lower(), headers=header)
        j = r.json()
        sauce = j['metadata']['provider']
        
        

    def message(self, message):
        self.time = time.time()
        self.log('stranger', message)
        print '\nStranger %s: %s' % (self.random_id, message)
        self.chats += 1
        self.analyze(message)
        
    def analyze(self, message):
        if any([x in message for x in ['*their', "*they're",'*there', '*your',"*you're"]]):
            print('Message flagged')
            #self.out('*Notice* Warning you have been flagged for pedantry')
            #self.out("Pedantry is a sign of intellectual insecurity") 
            #self.out("Your attempt to discredit someone through non-relevant attention to detail (probably classist based) only reveals your insecurities about your capacity to think critically and focus on the content") 
        elif any([x in message for x in ['*their', "*they're",'*there', '*your',"*you're"]]):
            self.out('*Notice* Warning you have been flagged for being underaged')
            self.out('*Notice* Please let your parents know you are online without their permission')
            h.on = False
        elif all(["Captcha" in message, "migrate" in message, "Omegle" in message]):
            c.next()
        elif all([("she" or 'mmm' or 'so') in message, ("add" or "snap" or 'ghost') in message]):
            c.next()
          
            
    def timer(self):
        if self.verbose:
            print('Service: timer started\n')
        t = time.time()
        while True:
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
    elif any([True for x in ['\\timer', '\\t'] if x in input_str.strip()]):
        h.tout = int(''.join([x for x in input_str.strip() if x.isdigit()]))
        print('h.tout set to: %s'%h.tout)
    elif input_str.strip() in ['\\verbose', '\\v']:
        h.verbose = True
        print('Service: verbose mode on')
    elif any([True for x in ['\\opener', '\\o'] if x in input_str.strip()]):
        h.opener = xin(input_str.strip())
    elif any([True for x in ['\\spam'] if x in input_str.strip()]):
        for _ in range(20):
            h.out(xin(input_str.strip()), verbose)
    elif any([True for x in ['\\d'] if x in input_str.strip()]):
        h.out(h.define(xin(input_str.strip())), verbose)
    elif any([True for x in ['\\c'] if x in input_str.strip()]):
        h.out(h.c)
    else:
        if h.on == True:
            h.out(input_str, verbose)
