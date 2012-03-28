#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: O_Menda (quegrande.org), Diz (diz.es), Santa
# Version: 0, (cerocoma)

#FIXME: Could be useless imports.
import sys
import socket
import string
import os
from commands import *


class SetOfCommands:
  def __init__(self):
    stallmanCommand = QuoteCommand("stallman", "stallman.txt")
    battleCommand = BattleCommand("batalla")
    fortuneCommand = FortuneCommand("galletita")
    dummyAnswerCommand = DummyAnswerCommand("zas")
    dummyAnswerCommand.setDummyAnswer("¡¡¡En toda la boca!!!")
    echoCommand = EchoCommand("eco")
    self.dict = {"stallman":stallmanCommand, "batalla":battleCommand, \
      "galletita":fortuneCommand, "zas":dummyAnswerCommand, "eco":echoCommand}

  def getCommand(self, stringCommand):
    try:
      result = self.dict[stringCommand]
      return result
    except KeyError:
      return None


class QGBot:
  def __init__(self, server, port, channel, nick, debug = False):
    self.server = server
    self.port = port
    self.channel = channel
    self.nick = nick
    self.debug = debug
    self.socket = socket.socket()
    self.socket.connect((server, port))
    self.socket.send('NICK ' + nick + '\r\n')
    self.socket.send('USER QGBot quegrande.org qgbot :O_Menda\r\n')
    self.socket.send('JOIN ' + channel + '\r\n')
    self.isBattleSet = False
    self.setOfCommands = SetOfCommands()
    self.lastCommand = None

  def printDebug(self, m):
    if self.debug:
      sys.stdout.write(m)

  def sendChannelMessage(self, m):
    messageLines = m.split('\n')
    for l in messageLines:
      self.socket.send('PRIVMSG ' + self.channel + ' :' + l + '\r\n')

  def sendFortune(self):
    f = os.popen("fortune -s")
    while True:
      line = f.readline()
      if not line: break
      else: self.sendChannelMessage(line)

  def processMessage(self, s, m):
    if m.startswith('!'):
      m = m.replace('!','',1)
      m = m.replace('\n','',1).replace('\r','',1)
      args = m.split(" ")
      if (self.lastCommand == None) or (self.lastCommand.isFinished()):
        self.lastCommand = self.setOfCommands.getCommand(args[0])
        if self.lastCommand != None:
          self.sendChannelMessage(self.lastCommand.execute(s,args))
        else:
          self.printDebug('Me mandaron hacer ' + m + '\n')
          self.sendChannelMessage('Tampoco te pases, ' + s)
      else:
        self.sendChannelMessage(self.lastCommand.execute(s,args))

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
          self.processMessage(sender, message)

  def die(self, s):
    if s != 'O_Menda': return
    self.socket.send('PART ' + self.channel + '\r\n')
    self.socket.send('QUIT\r\n')
    self.socket.close()
    sys.exit

if __name__ == "__main__":
  bot = QGBot('chat.eu.freenode.net', 7000, '#quegrande', 'Willy_Bromas', True)
  bot.loop()
