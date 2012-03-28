#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: Diz (diz.es)
# Version: sqrt(-1^3) (Advanced imaginary sketching phase)

import re
import urllib2
import xml.parsers.expat
from xml.dom import minidom

class LastFM:
  pattern = "!lastfm(?: (.+))?"

  def __init__(self, f):
    self.output = f
    reg = re.compile("(.+) -> (.+)")
    self.users = {}
    f = open('data/lastfm.users','r')
    for line in f.readlines():
      m = reg.match(line)
      if m != None:
        self.users[m.group(1)] = m.group(2)
    f.close()

  def checkUser(self, name):
    url = 'http://ws.audioscrobbler.com/1.0/user/' + name + '/recenttracks.xml'
    f = urllib2.build_opener().open(url)
    s = f.read()
    f.close()
    try:
      d = minidom.parseString(s)
      artists = d.getElementsByTagName('artist')
      songs = d.getElementsByTagName('name')
      if (len(artists) > 3): length = 3
      else: length = len(artists)
      for i in range(0, length):
        a = artists[i].firstChild.data.encode('utf8')
        s = songs[i].firstChild.data.encode('utf8')
        self.output(s + " (" + a + ")");
    except xml.parsers.expat.ExpatError:
      self.output('No existe ese usario en LastFM')

  def run(self, msg, who):
    m = re.compile(self.pattern).match(msg)
    if m.group(1) != None: self.checkUser(m.group(1))
    elif self.users.has_key(who): self.checkUser(self.users[who])
    else: self.checkUser(who)
