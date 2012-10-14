#!/usr/bin/env python
#coding=utf-8

import re
from random import randint

class Dice:
    
    def __init__(self, bot):
        self._bot = bot


    def listen(self, nick, msg):  
        if not msg.startswith("roll "):
            return
        msg = msg[5:] 
             
        result = 0
        regex = re.compile("([-+])?(?:(\d+)(d)?(\d+)?)", re.IGNORECASE)
        
        for match in regex.finditer(msg):
            if match.group(1) == "-":
                factor = -1
            else:
                factor = 1
            if match.group(3) == "d":
                value = self.roll(int(match.group(2)), int(match.group(4)))
            else:
                value = int(match.group(2))
            result += factor * value

        self._bot.talk(str(result))


    def roll(self, num, sides):
        if (sides == 0): return 0
        n = 0;
        for die in range(num): n += randint(1,sides)
        return n