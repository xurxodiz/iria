#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: Diz (diz.es)
# Version: sqrt(-1) (Still imaginary sketching phase)

from bot import Bot
from zap import Zap
from ppt import PPT
from lastfm import LastFM
from stallman import Stallman
from dice import Dice
from forumposts import ForumPosts
from batalla import Batalla
from minicity import Minicity
from chispa import Chispa

b = Bot('irc.cambred', 6667, '#CambRED', '[QG]iria_')

l = [
      Zap(b.talk),
      PPT(b.talk),
      LastFM(b.talk),
      Stallman(b.talk),
      Dice(b.talk),
      ForumPosts(b.talk),
      Batalla(b.talk),
      Minicity(b.talk),
      Chispa(b.talk)
    ]

b.loadModuleList(l)

"""
m = Zap(b.talk)
b.loadModule(m)
m = PPT(b.talk)
b.loadModule(m)
m = LastFM(b.talk)
b.loadModule(m)"""

b.loop()
