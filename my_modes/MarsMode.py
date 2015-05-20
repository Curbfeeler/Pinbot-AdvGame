import procgame.game
import pygame
import my_modes
import random
from pygame.locals import *
from pygame.font import *
from my_modes import PlanetMode

class MarsMode(PlanetMode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(PlanetMode, self).__init__(game=game, priority=40)
    self.iPlanetTickCounter = 120
    self.iSpecialTickCounter = 60
    self.bSpecialCountdown = False
    self.strPlanetVoice = 'mars_redplanet'
    self.strPlanetName = 'Mars'
    self.strPlanetDisplayText = ['Welcome to Mars', '', 'Make the VORTEX for 10x Scoring!']
    pass

  def checkHit(self, num, myScore = 0):
      if(num == -1):
          self.game.sound.play('target')
          self.game.score(100)
      else:
        if self.game.switches.enterRamp.time_since_change() < 10 and self.game.switches.exitRamp.time_since_change() < 9  and self.game.switches.shooter.time_since_change() < 8 :
          self.SuccessHelper()

  def sw_vortex5k_active(self, sw):
      self.checkHit(1, 5000)
      return procgame.game.SwitchContinue

  def sw_vortex20k_active(self, sw):
      self.checkHit(1, 20000)
      return procgame.game.SwitchContinue

  def sw_vortex100k_active(self, sw):
      self.checkHit(1, 100000)
      return procgame.game.SwitchContinue
  
