#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: O_Menda (quegrande.org)
# Version: 0.66b

import re
import time
import urllib2
import thread
from xml.dom import minidom

class ForumPosts:
  pattern = "!(foro|mafia)"

  def __init__(self, f):
    self.output = f
    self.messages = {}
    self.time = {}
    thread.start_new_thread(self.checkNumber,("foro",))
    thread.start_new_thread(self.checkNumber,("mafia",))

  def checkNumber(self, forum):
    w = urllib2.build_opener().open('http://quegrande.org/' + forum + '/')
    t = w.read()
    w.close()
    check = 2;
    if forum == 'mafia': check = 3
    self.messages[forum] = int(minidom.parseString(t).getElementsByTagName('strong')[check].firstChild.data.encode('utf8'))
    self.time[forum] = time.time()

  def run(self, msg, who):
    m = re.compile(self.pattern).match(msg)
    forum = m.group(1)
    n = self.messages[forum]
    t = self.time[forum]
    self.checkNumber(forum)
    n = self.messages[forum] - n
    t = self.time[forum] - t
    self.output(str(n) + " mensajes desde la última comprobación hace " + str(int(t)) + " segundos")