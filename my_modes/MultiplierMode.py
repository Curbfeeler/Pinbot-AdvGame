import procgame.game
import pygame
import my_modes
from pygame.locals import *
from pygame.font import *
from procgame.game import AdvancedMode

class MultiplierMode(AdvancedMode):

  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(MultiplierMode, self).__init__(game=game, priority=10, mode_type=AdvancedMode.Ball)
    self.multiplier = 1 
    pass

  def mode_started(self):
    print("SS: skill shot mode began.")
    self.update_lamps()

  def endMode(self):
    self.game.modes.remove(self)

  def mode_stopped(self):  # naming is inconsistent with game_ended/ball_ended
#    self.game.modes.add(self.game.chest_mode)
    print("SS: skill shot mode complete.")

  def update_lamps(self):
    #### Get Multiplier ####
    #self.multiplier = self.game.utilities.get_player_stats('bonus_x')

    #### Clear Lamps ####
    self.game.lamps.x2Bonus.disable()
    self.game.lamps.x3Bonus.disable()
    self.game.lamps.x4Bonus.disable()
    self.game.lamps.x5Bonus.disable()

    if (self.multiplier > 1):
        self.game.lamps.x2Bonus.enable()
    if (self.multiplier > 2):
        self.game.lamps.x3Bonus.enable()
    if (self.multiplier > 3):
        self.game.lamps.x4Bonus.enable()
    if (self.multiplier > 4):
        self.game.lamps.x5Bonus.enable()

  def incrementBonusMultiplier(self):
    if (self.multiplier <> 5):
      self.multiplier = self.multiplier + 1
      self.game.sound.play('bonus_mult')
      self.game.displayText("BONUS X" +str(self.multiplier))
      self.update_lamps()
    else:
        #### Bonus Maxed ####
        pass

  def sw_exitRamp_closed(self, sw):
    if self.game.switches.enterRamp.time_since_change() < 3:
        self.incrementBonusMultiplier()
    return procgame.game.SwitchContinue        
    
  def sw_shooter_active_for_200ms(self, sw):
    if self.game.switches.exitRamp.time_since_change() < 8:
        print self.game.switches.exitRamp.time_since_change()
        #self.game.modes.add(self.game.vortex_mode)
    return procgame.game.SwitchContinue    

