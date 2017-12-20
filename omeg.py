from pyomegle import OmegleClient, OmegleHandler
import time
import os
import random
import sys
import select


class Hand(OmegleHandler):
    def __init__(self, *args, **kwargs):
        OmegleHandler.__init__(self, *args, **kwargs)
        self.random_id = 0
        self.chats = 0
        self.upool = set([0])
        self.uhist = {'stranger': [], 'user': [], 'collective': []}
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
        self.message(input_str.strip())
        if verbose:
            pass  # print 'timer was at %s' % (time.time() - timer)
        if input_str.strip():
            pass  # timer = time.time()
        if verbose:
            pass  # print "Timer reset to %s" % (time.time() - timer)
        if verbose:
            pass

    def log(self, pers, text):
        self.hist[self.random_id][pers].append(text)
        self.hist[self.random_id]['collective'].append(text)

    def connected(self):
        os.system('clear')
        print 'You\'re now chatting with a random stranger. Say hi!'
        while self.random_id in self.upool:
            self.random_id = random.randint(100000, 999999)
        self.upool.add(self.random_id)
        self.hist[self.random_id] = self.uhist
        print 'They\'ve been assigned the username: %s' % (self.random_id)

    def message(self, message):
        self.timer = time.time()
        self.log('stranger', message)
        print '\nStranger %s: %s' % (self.random_id, message)
        self.chats += 1


h = Hand(loop=True)  # session loop
c = OmegleClient(h, wpm=47, lang='en', topics=[
                 'politic', 'political', 'politics', 'trump'])
# 47 words per minute
c.start()

read_list = [sys.stdin]
timeout = 0.1  # seconds
verbose = False
while 1:
    ready = select.select(read_list, [], [], timeout)[0]
    if ready:
        for file in ready:
            input_str = file.readline()
        if input_str.strip() == '\\next':
            c.next()
        elif input_str.strip() == '\\exit':
            c.disconnect()  # disconnect chat session break
            exit()
        elif input_str.strip() in ['\\h', '\\help']:
            print helpt
        elif input_str.strip() == '\\verbose':
            verbose = True
        else:
            h.out(input_str, verbose)
