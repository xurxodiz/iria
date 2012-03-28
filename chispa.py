#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: O_Menda (quegrande.org)
# Version: chispa.0

class Chispa:
  pattern = ".*"

  def __init__(self, f):
    self.output = f
    self.lastMessage = ""
    self.lastUer = None

  def run(self, msg, who):
    if self.lastMessage == msg and self.lastUser != who:
      self.output('Â¡Chispa!')
      self.lastMessage = "ÂChispa!"
      self.lastUser = "iria_"
      # chapuza
      # sanitize and such
    else:
      self.lastMessage = msg
      self.lastUser = who
