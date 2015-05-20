import procgame.game
import pygame
import my_modes
import random
from pygame.locals import *
from pygame.font import *
from my_modes import PlanetMode

class PlutoMode(PlanetMode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(PlanetMode, self).__init__(game=game, priority=40)
    self.iTotalPops = 0
    self.iPlanetTickCounter = 30
    self.iSpecialTickCounter = 60
    self.bSpecialCountdown = False
    self.strPlanetVoice = 'pluto_dwarf'
    self.strPlanetName = 'Pluto'
    self.strPlanetDisplayText = ['Welcome to Pluto', '', '20 Pops in 30 Seconds!']
    pass

  def checkHit(self, num):
      if(num == -1):
          self.game.sound.play('target')
          self.game.score(100)
      else:
          self.iTotalPops = self.iTotalPops + 1
          if(self.iTotalPops == 20):
              self.SuccessHelper()
          else:
            self.game.score(1000)
            list1 = [str(self.iTotalPops) +'!' ,'', 'Only ' +str(20-self.iTotalPops) +' to go!']
            self.game.displayText(list1)

  def sw_jetTop_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop

  def sw_jetMiddle_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop

  def sw_jetBottom_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop