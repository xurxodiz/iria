#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: Diz (diz.es)
# Version: sqrt(-1) (Still imaginary sketching phase)

import re

class Zap:

  _fapregex = "^([.]+\w)?paja[s]?(\w[.]+)?$"
  pattern = "(!(zas|fap|orly|fuckyeah|eco (.*))|" + _fapregex + ")"

  def __init__(self, f):
    self.output = f

  def run(self, msg, who):
    m = re.compile(self.pattern).match(msg)
    if m.group() == "!zas": self.output('En toda la cavidad bucal')
    elif m.group() == "!orly": self.output('Ya rly!')
    elif m.group() == "!fuckyeah": self.output('SEAKING DESTROY!')
    elif m.group().startswith("!eco"): self.output(m.group(3))
    else: self.output('fap fap fap')
