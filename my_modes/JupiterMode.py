import procgame.game
import pygame
import my_modes
import random
from pygame.locals import *
from pygame.font import *
from my_modes import PlanetMode

class JupiterMode(PlanetMode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(PlanetMode, self).__init__(game=game, priority=40)
    self.iPlanetTickCounter = 30
    self.iSpecialTickCounter = 60
    self.bSpecialCountdown = False
    self.strPlanetVoice = 'jupiter_redeyegiant'
    self.strPlanetName = 'Jupiter'
    self.strPlanetDisplayText = ['Welcome to Jupiter', '', 'Seek shelter from the Red Storm']
    pass

  def checkHit(self, num):
      if(num == -1):
          self.game.sound.play('target')
          self.game.score(100)
      else:
        self.SuccessHelper()

  def sw_scoreEnergyStandUp_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop
