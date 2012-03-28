#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: O_Menda (quegrande.org)
# Version: 0.99
# TODO: Aceptar restas en al menos el último operando

import re
from random import randrange

class Dice:
  pattern = "!((?:\+?\d+d\d+)+)(?:\+(\d)*)?"

  def __init__(self, f):
    self.output = f

  def roll(self, num, sides):
    if (sides == 0): return 0
    n = 0;
    for die in range(num): n += randrange(sides)+1
    return n

  def run(self, msg, who):
    m = re.compile(self.pattern).match(msg)
    p = re.compile("(\d+)d(\d+)")
    result = 0
    for exp in m.group(1).split("+"):
      n = p.match(exp)
      result += self.roll(int(n.group(1)), int(n.group(2)))
    if m.lastindex == 2: result += int(m.group(2))
    self.output("Resultado para " + who +": " + str(result))