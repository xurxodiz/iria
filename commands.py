#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: O_Menda (quegrande.org), Diz (diz.es), Santa
# Version: 0, (cerocoma)

#FIXME: Might contain useless imports.
import string
import os
import time
import random
import urllib2
import xml.parsers.expat
from xml.dom import minidom

class Command:

  def __init__(self, commandName):
    self.commandName = commandName

  def getName(self):
    return self.commandName

  def execute(self, sender, args):
    return ""

  def isFinished(self):
    return True


class FileQuote:

  def __init__(self, fil, dir='data/quotes/'):
    self.quoteList = open(dir+fil).readlines()

  def getRandom(self):
    return random.choice(quoteList)


class QuoteCommand(Command):

  def __init__(self, commandName, fileName):
    Command.__init__(self, commandName)
    self.quotes = FileQuote(fileName)

  def execute(self, sender, args):
    return self.quotes.getRandom()


class BattleCommand(Command):

  def __init__(self, commandName):
    self.commandName = commandName
    self.status = -1

  def execute(self, sender, args):
    self.status += 1
    result = ""
    if self.status == 0:
      # FIXME: Index out of bounds when typing the command without arguments.
      self.battle = args[1]
      f = urllib2.build_opener().open('http://quegrande.org/batalla/' + self.battle)
      t = f.read()
      f.close()
      try:
        d = minidom.parseString(t)
        self.c1 = d.getElementsByTagName('h3')[0].firstChild.data.encode('utf8')
        self.c2 = d.getElementsByTagName('h3')[1].firstChild.data.encode('utf8')
        self.i1 = d.getElementsByTagName('input')[0].getAttribute('value')
        self.i2 = d.getElementsByTagName('input')[1].getAttribute('value')
        result += '1. ' + self.c1 + '\n'
        result += '2. ' + self.c2 + '\n'
        result += 'Votad escribiendo !1 ó !2'
        self.votes = {}
      except xml.parsers.expat.ExpatError:
        result += 'Esa batalla no existe, tangante'
      except IndexError:
        result += 'Petó la batalla con un IndexError'
    elif self.status == 1:
      self.status = -1
      vote = args[0]
      if vote == '1' or vote == '2': self.votes[sender] = vote
      v1 = 0
      v2 = 0
      for v in self.votes.keys():
        if self.votes[v] == '1': v1+=1
        else: v2+=1
      f = open('logs/batalla/'+ self.battle + '.log', 'a')
      if v1>v2:
        f.write(self.i1 + ' / ' + self.i2 + '\n')
        result += 'Ha ganado ' + self.c1
      elif v2>v1:
        f.write(self.i2 + ' / ' + self.i1 + '\n')
        result += 'Ha ganado ' + self.c2
      else:
        result += 'Ha habido empate en la batalla ' + self.battle
      f.close()
    return result

  def isFinished(self):
    return self.status == -1


class FortuneCommand(Command):

  def __init__(self, commandName):
    Command.__init__(self, commandName)

  def execute(self,sender,args):
   f = os.popen("fortune -s") 
   result = ""
   while True:
     line = f.readline()
     if not line: break
     else: result += line + '\n'
   return result


class EchoCommand(Command):
  def __init__(self,commandName):
    Command.__init__(self,commandName)

  def execute(self,sender,args):
    result = ""
    for i in args:
      result += i + " "
    return result


class MailCommand(Command):
  def __init__(self,commandName):
    Command.__init__(self.commandName)
    self.queue = {}

  def execute(self,sender,args):
    try: [r, m] = m.split(' ', 1)
    except ValueError: return 'Formato correcto: !msg nick mensaje'
    msg = 'Mensaje de ' + sender + ' escrito el ' + \
      time.ctime(time.time()) + ':\n' + args
    if self.queue.has_key(r): self.queue[r] = msg
    else: self.queue[r] += '\n' + msg
    self.sendQueuedMessages()
    return ''

  #def sendQueuedMessages(self):
  #  for user in self.queue.keys():
  #    if user in self.userList:
  #      self.sendPrivateMessage(user, self.queue[user])

class DummyAnswerCommand(Command):
  #Because dummy commands begin people happy XD
  def __init__(self,commandName):
    Command.__init__(self,commandName)
    self.dummyAnswer = "Dummy Answer for you."

  def getDummyAnswer(self):
    return self.dummyAnswer

  def setDummyAnswer(self,answer):
    self.dummyAnswer = answer

  def execute(self,sender,args):
    return self.dummyAnswer
