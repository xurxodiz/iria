#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: Diz (diz.es)
# Version: sqrt(-1) (Still imaginary sketching phase)

import re
import random
from frases import Frases

class Stallman(Frases):

  pattern = ""

  def __init__(self, f):
    Frases.__init__(self, f, ["!stallman", "data/quotes/stallman.txt"])
