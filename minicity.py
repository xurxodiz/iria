#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: O_Menda (quegrande.org)
# Version: 0.8

import re
import urllib2
from xml.dom import minidom

class Minicity:
  pattern = "!mini(?: (.+))?"

  def __init__(self, f):
    self.output = f

  def checkNeeds(self, city):
    url = 'http://' + city + '.myminicity.es/'
    try:
      w = urllib2.build_opener().open(url + 'xml')
      t = w.read()
      w.close()
      d = {}
      d['ind'] = int(minidom.parseString(t).getElementsByTagName('unemployment')[0].firstChild.data)
      d['tra'] = 100-int(minidom.parseString(t).getElementsByTagName('transport')[0].firstChild.data)
      d['sec'] = int(minidom.parseString(t).getElementsByTagName('criminality')[0].firstChild.data)
      d['env'] = int(minidom.parseString(t).getElementsByTagName('pollution')[0].firstChild.data)
      maxi = max([(d[x],x) for x in d])
      if maxi[0] == 0: self.output('La miniciudad de ' + city + ' no tiene ninguna necesidad especial, mejora lo que quieras: ' + url)
      else: self.output('Ahora mismo ' + city + ' necesita ' + url + maxi[1])
    except:
      self.output('No se pudo acceder a la información de ' + url)

  def run(self, msg, who):
    m = re.compile(self.pattern).match(msg)
    if m.group(1) == None: self.checkNeeds("quegrande.org")
    else: self.checkNeeds(m.group(1))
