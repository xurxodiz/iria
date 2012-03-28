#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: Diz (diz.es)
# Version: sqrt(-1) (Still imaginary sketching phase)

import re
import random

class Frases:

  pattern = ""

  def __init__(self, f, l):
    self.output = f
    try:
      self.pattern = l[0] 
      self.quotes = open(l[1]).readlines()
    except:
      self.output("Error de parámetros al inicializar el módulo de frases: " + l)

  def run(self, msg, who):
    self.output(random.choice(self.quotes))
