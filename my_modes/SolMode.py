import procgame.game
import pygame
import my_modes
from pygame.locals import *
from pygame.font import *

class SolMode(procgame.game.Mode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(SolMode, self).__init__(game=game, priority=40)
    self.iSolTickCounter = 30
    self.iSpecialTickCounter = 12
    self.bSpecialCountdown = False
    pass

  def mode_started(self):
    print("SS: skill shot mode began.")
    self.game.modes.remove(self.game.chest_mode)
    self.game.modes.remove(self.game.droptargets_mode)
    self.SuccessAdvancePlanetLightShow()
    self.game.sound.play_music('Sol')
    self.game.displayText("Welcome to Sol.  30 seconds to hit the pops from the left ramp!")
    self.solTick()

  def endMode(self):
    self.game.modes.remove(self)


  def mode_stopped(self):  # naming is inconsistent with game_ended/ball_ended
    self.game.sound.fadeout_music()
    #self.game.setPlayerState(self, key='lastPlanetVisited', val='Sol')
    self.game.lastPlanetVisited = 'Sol'
    self.game.lamps.specialLamp.disable()
    if self.game.chest_mode in self.game.modes:
                self.game.displayText("Removing Chest")
                self.game.modes.remove(self.game.chest_mode)
    self.game.modes.add(self.game.chest_mode)
    if self.game.droptargets_mode in self.game.modes:
                self.game.displayText("Removing droptargets_mode")
                self.game.modes.remove(self.game.droptargets_mode)
    self.game.modes.add(self.game.droptargets_mode)    
    
#    self.game.modes.add(self.game.chest_mode)
    print("SS: skill shot mode complete.")

  def checkHit(self, num):
      if(num == -1):
          self.game.sound.play('laser')
          self.game.score(100)
      elif self.game.switches.enterRamp.time_since_change() < 6 and self.game.switches.exitRamp.time_since_change() < 5:
            self.game.score(50000)
            self.SuccessAdvancePlanetLightShow()
            self.game.displayText('The Sun is yours!  Hurry To Make Special...', duration = 5)
            self.bSpecialCountdown = True
            self.delay(name='specialTick',
              event_type=None,
              delay=2,
              handler=self.specialTick)


  def solTick(self):
      self.iSolTickCounter = self.iSolTickCounter - 1
      if (self.iSolTickCounter % 5 == 0 or self.iSolTickCounter < 5):
        self.game.displayText(['HURRY' , '',  str(self.iSolTickCounter) +' Seconds Left!!!'])
      if self.iSolTickCounter == 0:
          self.endMode()
          return
      self.delay(name='solTick',
        event_type=None,
        delay=1,
        handler=self.solTick)

  def specialTick(self):
          self.iSpecialTickCounter = self.iSpecialTickCounter - 1
          if self.iSpecialTickCounter % 2 == 0:
              self.game.lamps.specialLamp.enable()
          else:
              self.game.lamps.specialLamp.disable()
          if (self.iSpecialTickCounter % 5 == 0 or self.iSpecialTickCounter < 5):
            self.game.displayText(['HURRY' , '',  str(self.iSpecialTickCounter) +' Seconds Left!!!'])
          if self.iSpecialTickCounter == 0:
              self.endMode()
              return
          self.delay(name='specialTick',
            event_type=None,
            delay=1,
            handler=self.specialTick)

  def checkSpecialHit(self, num):
      if(num == -1):
          self.game.sound.play('laser')
          self.game.score(100)
      else:
        self.game.score(50000)
        self.game.displayText('Special Awarded', duration = 5)
        self.delay(name='endmode',
            event_type=None,
            delay=1,
            handler=self.endMode)

  def SuccessAdvancePlanetLightShow(self):
    self.game.lamps.pluto.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.neptune.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.uranus.schedule(schedule=0x0000ffff, cycle_seconds=3, now=False)
    self.game.lamps.saturn.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.jupiter.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.mars.schedule(schedule=0x0000ffff, cycle_seconds=3, now=False)
    self.game.lamps.earth.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.venus.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.mercury.schedule(schedule=0x0000ffff, cycle_seconds=3, now=False)
      

  def sw_vortex5k_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchContinue

  def sw_vortex20k_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchContinue

  def sw_vortex100k_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchContinue
  
  def sw_chestMatrix01_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop
  
  def sw_chestMatrix02_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_chestMatrix03_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_chestMatrix04_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_chestMatrix05_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_chestMatrix10_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_chestMatrix20_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop
  
  def sw_chestMatrix30_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop
  
  def sw_chestMatrix40_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop
  
  def sw_chestMatrix50_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_slingR_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_slingL_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_outlaneLeft_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_inlaneLeft_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_inlaneRight_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_outlaneRight_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_singleEject_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_enterRamp_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_jetTop_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop

  def sw_jetMiddle_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop

  def sw_jetBottom_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop

  def sw_tenPointer1_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_tenPointer2_BehindDropBank_active(self, sw):
      self.game.coils.dropTargetReset_RightInsertBDFlasher.pulse(150)   
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_tenPointer3_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_upperDrop_active(self, sw):
      self.game.coils.dropTargetReset_RightInsertBDFlasher.pulse(150)   
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_midDrop_active(self, sw):
      self.game.coils.dropTargetReset_RightInsertBDFlasher.pulse(150)   
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_lowerDrop_active(self, sw):
      self.game.coils.dropTargetReset_RightInsertBDFlasher.pulse(150)   
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_scoreEnergyStandUp_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_advancePlanent_active(self, sw):
      if self.bSpecialCountdown == True:
          self.checkSpecialHit(1)
      else:
          self.checkHit(-1)
      return procgame.game.SwitchStop
