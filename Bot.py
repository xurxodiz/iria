#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: Diz (diz.es)
# Version: sqrt(-1) (Still imaginary sketching phase)

import thread
from modules.Dice import Dice
from modules.Spark import Spark

class Bot(object):
    def __init__(self, room, nick, client):
        self.room = room
        self.nick = nick
        self.client = client
        self._loadModules()

    def talk(self, msg):
        self.client(self.room, msg)
      
    def listen(self, nick, msg):
        for m in self._modules:
            thread.start_new_thread(m.listen, (nick, msg))
    
    def _loadModules(self):
        self._modules = [
            Dice(self),
            Spark(self)
        ]
