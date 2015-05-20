import procgame.game
import pygame
import my_modes
import random
from pygame.locals import *
from pygame.font import *
from my_modes import PlanetMode

class SaturnMode(PlanetMode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(PlanetMode, self).__init__(game=game, priority=40)
    self.iSaturnLoops = 0
    self.iPlanetTickCounter = 120
    self.iSpecialTickCounter = 60
    self.bSpecialCountdown = False
    self.strPlanetVoice = 'saturn_ringed'
    self.strPlanetName = 'Saturn'
    self.strPlanetDisplayText = ['The Saturn Ring Challenge', '', '3 Rings from Left Ramp']
    pass

  def checkHit(self, num):
      if(num == -1):
          self.game.sound.play('target')
          self.game.score(100)
      else:
        if self.game.switches.enterRamp.time_since_change() < 6 and self.game.switches.exitRamp.time_since_change() < 5:
            self.iSaturnLoops = self.iSaturnLoops + 1
            if (self.iSaturnLoops < 3):
                self.game.score(10000)
                self.game.displayText(str(self.iSaturnLoops) +' Rings!', duration = 5)
            else:
              self.SuccessHelper()

  def sw_inlaneRight_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop

