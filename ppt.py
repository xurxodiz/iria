#!/usr/bin/env python
#coding=utf-8

# GPLv3: http://www.gnu.org/copyleft/gpl.html
# Authors: Diz (diz.es)
# Version: sqrt(-1) (Still imaginary sketching phase)

import re
import random
import time

class PPT:

  pattern = "!(ppt|piedra|papel|tijera)"
  
  ROCK = 1
  PAPER = 2
  SCISSORS = 3
  
  WIN = 1
  TIE = 0
  LOSE = -1
  
  grid = { ROCK : { ROCK : TIE, PAPER : LOSE, SCISSORS: WIN },
           PAPER : { ROCK : WIN, PAPER : TIE, SCISSORS : LOSE },
           SCISSORS : { ROCK: LOSE, PAPER : WIN, SCISSORS : TIE } }

  def __init__(self, f):
    self.output = f
    self.reset()
    
  def countdown(self, t):
    while t > 0:
      self.output('%i...' % t)
      time.sleep(1)
      t -= 1
    self.choose()
      
  def choose(self):
    l = [self.ROCK, self.PAPER, self.SCISSORS]
    i = random.randint(0,2)
    self.election = l[i]
    if self.election == self.ROCK: self.output('Piedra!')
    elif self.election == self.PAPER: self.output('Papel!')
    elif self.election == self.SCISSORS: self.output('Tijera!')
    time.sleep(2)
    self.decideWinner()
    
  def startBattle(self, opponent):
    self.output('Bien, juguemos a Piedra/Papel/Tijera, %s' % opponent)
    self.oncourse = True
    self.opponent = opponent
    time.sleep(2)
    self.countdown(3)
    
  def opponentChooses(self, who, opt):
    if who == self.opponent:
      if opt == '!piedra': self.playerElection = self.ROCK
      elif opt == '!papel' : self.playerElection = self.PAPER
      elif opt == '!tijera' : self.playerElection = self.SCISSORS
      
  def reset(self):
    self.oncourse = False
    self.election = None
    self.opponent = None
    self.playerElection = None
    
  def decideWinner(self):
    if self.playerElection == None:
      self.output('¿No quieres jugar conmigo? :(')
    else:
      outcome = self.grid[self.election][self.playerElection]
      if outcome == self.WIN:
        self.output('Gané.')
      elif outcome == self.TIE:
        self.output('Empate! Va otra.')
        self.reset()
        self.start(self.opponent)
      else:
        self.output('Jo. Perdí.')
    self.reset()

  def run(self, msg, who):
    m = re.compile(self.pattern).match(msg)
    if m.group() == "!ppt" and not self.oncourse: 
      self.startBattle(who)
    elif not m.group() == "!ppt" and self.oncourse:
      self.opponentChooses(who, m.group())
