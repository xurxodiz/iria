#!/usr/bin/env python
#coding=utf-8

#!/usr/bin/env python
#coding=utf-8

import re
from random import randint

class Spark:
    
    def __init__(self, bot):
        self._bot = bot
        self._lastMessage = ""
        self._lastUser = None


    def listen(self, nick, msg):
        if nick == self._bot.nick:
            return
        if self._lastMessage == msg and self._lastUser != nick:
            self._bot.talk('spark!')
            self._lastMessage = "spark!"
            self._lastUser = "iria_"
        else:
            self._lastMessage = msg
            self._lastUser = nick
