#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: Diz (diz.es)
# Version: sqrt(-1) (Still imaginary sketching phase)

import sys
import socket
import re
import thread


class Bot:
  def __init__(self, server, port, channel, nick):
    self.server = server
    self.port = port
    self.channel = channel
    self.nick = nick
    self.socket = socket.socket()
    self.socket.connect((server, port))
    self.socket.send('NICK ' + nick + '\r\n')
    self.socket.send('USER ' + nick + ' ' + nick + ' ' + nick + ' :' + nick + '\r\n')
    self.socket.send('JOIN ' + channel + '\r\n')
    self.dic = {}

  def talk(self, m):
    messageLines = m.split('\n')
    for l in messageLines:
      self.socket.send('PRIVMSG ' + self.channel + ' :' + l + '\r\n')
      
  def parse(self, s, msg):
    msg = msg.strip()
    for p in self.dic.keys():
      m = p.match(msg)
      if m: thread.start_new_thread(self.dic[p].run, (msg, s))


  def loop(self):
    while True:
      data = self.socket.recv(4096)
      if data.find ('PING') != -1:
        self.socket.send ('PONG ' + data.split()[1] + '\r\n')
      elif data.find ('PRIVMSG') != -1:
        sender = data.split('!')[0].replace (':', '')
        message = ':'.join (data.split(':')[2:])
        destination = ''.join (data.split(':')[:2]).split(' ')[-2]
        if destination == self.channel:
          self.parse(sender, message)

  def die(self, msg):
    self.socket.send('PART ' + self.channel + '\r\n')
    self.socket.send('QUIT ' + msg + '\r\n')
    self.socket.close()
    sys.exit
    
  def loadModule(self, mod):
    self.dic[re.compile(mod.pattern)] = mod
    
  def loadModuleList(self, l):
    for m in l:
      self.loadModule(m)
