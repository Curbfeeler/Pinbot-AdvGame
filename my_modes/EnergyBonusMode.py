import procgame.game
import pygame
import my_modes
from pygame.locals import *
from pygame.font import *
from procgame.game import AdvancedMode

class EnergyBonusMode(AdvancedMode):

  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(EnergyBonusMode, self).__init__(game=game, priority=10, mode_type=AdvancedMode.Ball)
    self.energyBonus = 0
    pass

  def mode_started(self):
    print("SS: skill shot mode began.")


  def endMode(self):
    self.game.modes.remove(self)


  def mode_stopped(self):  # naming is inconsistent with game_ended/ball_ended
    print("SS: skill shot mode complete.")

  def jetMade(self):
    self.game.sound.play('jet')
    self.game.score(100)
    self.energyBonus = self.energyBonus + 1000
    list1 = [' ', 'ENERGY BONUS', '', str(self.energyBonus), ' ']
    self.game.displayText(msg = list1, duration = 1) 

  def sw_jetMiddle_active(self, sw):
    self.jetMade()
    return procgame.game.SwitchStop

  def sw_jetBottom_active(self, sw):
    self.jetMade()
    return procgame.game.SwitchStop

  def sw_jetTop_active(self, sw):
    self.jetMade()
    return procgame.game.SwitchStop