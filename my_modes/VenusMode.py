import procgame.game
import pygame
import my_modes
from pygame.locals import *
from pygame.font import *
from my_modes import PlanetMode

class VenusMode(PlanetMode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(PlanetMode, self).__init__(game=game, priority=40)
    self.iPlanetTickCounter = 55
    self.iSpecialTickCounter = 60
    self.bSpecialCountdown = False
    self.strPlanetVoice = 'venus_eveningstar'
    self.strPlanetName = 'Venus'
    self.strPlanetDisplayText = ['Venus', '', 'TBD Mode']
    pass

  def checkHit(self, num):
      if(num == -1):
          self.game.sound.play('laser')
          self.game.score(100)
      else:
        self.SuccessHelper()
