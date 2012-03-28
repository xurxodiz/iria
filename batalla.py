#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: O_Menda (http://quegrande.org)
# Version: 0.99

import re
import urllib2
import time
from xml.dom import minidom

class Batalla:
  pattern = "!(batalla \w+|1|2)"

  def __init__(self, f):
    self.output = f
    self.running = False
  
  def readyBattle(self, battle):
    self.running = True
    f = urllib2.build_opener().open('http://quegrande.org/batalla/' + battle)
    t = f.read()
    f.close()
    try:
      d = minidom.parseString(t)
      self.c1 = d.getElementsByTagName('h3')[0].firstChild.data.encode('utf8')
      self.c2 = d.getElementsByTagName('h3')[1].firstChild.data.encode('utf8')
      self.i1 = d.getElementsByTagName('input')[0].getAttribute('value')
      self.i2 = d.getElementsByTagName('input')[1].getAttribute('value')
      self.output('1. ' + self.c1)
      self.output('2. ' + self.c2)
      self.output('Votad con !1 ó !2')
      self.battle = battle
      self.votes = {}
      time.sleep(8)
      self.endBattle()
    except:
      self.output('Esa batalla no existe, cariño')
      self.running = False

  def writeLog(self, win, lose):
    f = open('data/batalla.log', 'a')
    f.write(self.battle + ": [" + time.asctime(time.localtime()) + "] " + str(win) + " / " + str(lose) + "\n")
    f.close()

  def endBattle(self):
    n1 = 0
    n2 = 0
    for v in self.votes.values():
      if v == '1': n1 += 1
      else: n2 += 1
    if n1 > n2:
      self.output('Ganó ' + self.c1)
      self.writeLog(self.i1, self.i2)
    elif n2 > n1:
      self.output('Ganó ' + self.c2)
      self.writeLog(self.i2, self.i1)
    else:
      self.output('Hubo un empate')
    self.running = False

  def vote(self, select, who):
    self.votes[who] = select

  def run(self, msg, who):
    m = re.compile(self.pattern).match(msg)
    if self.running and (m.group(1) == '1' or m.group(1) == '2'):
      self.vote(m.group(1), who)
    elif not self.running and m.group(1) != '1' and m.group(1) != '2':
      self.readyBattle(m.group(1).split()[1])
    else:
      self.output('Ese comando no viene a cuento ahora, amor')