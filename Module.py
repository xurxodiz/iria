#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: Jorge Diz
# Version: √-1

class Module(object):

	# Children classes have to reimplement it
	# here it is a reminder on how should it be
	def __init__(self, bot):
		self._bot = bot

	def listen(self, nick, msg):
		pass