import procgame.game
import pygame
import my_modes
import random
from pygame.locals import *
from pygame.font import *
from my_modes import PlanetMode

class NeptuneMode(PlanetMode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(PlanetMode, self).__init__(game=game, priority=40)
    self.iTotalPops = 0
    self.iPlanetTickCounter = 45
    self.iSpecialTickCounter = 60
    self.bSpecialCountdown = False
    self.strPlanetVoice = 'neptune_8th'
    self.strPlanetName = 'Neptune'
    self.strPlanetDisplayText = ['Welcome to Neptune','', 'Enter Pops from Left Ramp']    
    pass

  def checkHit(self, num):
      if(num == -1):
          self.game.sound.play('target')
          self.game.score(100)
      elif self.game.switches.enterRamp.time_since_change() < 6 and self.game.switches.exitRamp.time_since_change() < 5:
          self.SuccessHelper()

  def sw_jetTop_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop

  def sw_jetMiddle_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop

  def sw_jetBottom_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop
