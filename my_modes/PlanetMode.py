import procgame.game
import pygame
import my_modes
import random
from pygame.locals import *
from pygame.font import *


class PlanetMode(procgame.game.Mode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def mode_started(self):
#    print('Planet Mode: '+self.strPlanetName +' began.')
    self.game.droptargets_mode.EnergyTickActive = False
    self.successAdvancePlanetLightShow()
    self.delay(delay=3, handler=self.delayed_blahblah)
    self.game.displayText(self.strPlanetDisplayText, duration=5)
    self.game.sound.play(self.strPlanetVoice)
    self.game.sound.play_music(self.strPlanetName)
    self.delay(delay=5, handler=self.delayed_blahblah)
    self.planetTick()

  def delayed_blahblah(self):
    print("It's been 1000 milliseconds!")

  def mode_stopped(self):  # naming is inconsistent with game_ended/ball_ended
    #self.game.setPlayerState(self, key='lastPlanetVisited', val='Pluto')
    self.disableModeLamps()
    self.game.lastPlanetVisited = self.strPlanetName
    self.game.lamps.specialLamp.disable()
    self.game.droptargets_mode.EnergyTickActive = True
    self.game.droptargets_mode.dtEnergyTick()
    self.game.droptargets_mode.dtAdvPlanentTick()

  def endMode(self):
    self.game.modes.remove(self)

  def disableModeLamps(self):
    pass

  def planetTick(self):
    if self.bSpecialCountdown == False:      
      self.iPlanetTickCounter = self.iPlanetTickCounter - 1
      if (self.iPlanetTickCounter == 10):
        self.game.sound.play('10_seconds')
      if (self.iPlanetTickCounter % 5 == 0 or self.iPlanetTickCounter < 5):
        self.game.displayText(['HURRY' , '',  str(self.iPlanetTickCounter) +' Seconds Left!!!'])
      if self.iPlanetTickCounter == 0:
        self.game.sound.fadeout_music()
        self.game.sound.play('miss_shot')
        self.game.sound.play_music('MainAfterMode' +str(self.game.ball) +'_' +str(random.randint(1,3)), loops=5)
        self.endMode()
        return
      self.delay(name='planetTick',
        event_type=None,
        delay=1,
        handler=self.planetTick)
    else:
        pass

  def specialTick(self):
          self.iSpecialTickCounter = self.iSpecialTickCounter - 1
          if self.iSpecialTickCounter % 2 == 0:
              self.game.lamps.specialLamp.enable()
          else:
              self.game.lamps.specialLamp.disable()
          if (self.iSpecialTickCounter == 10):
            self.game.sound.play('10_seconds')
          if (self.iSpecialTickCounter % 5 == 0 or self.iSpecialTickCounter < 5):
            self.game.displayText(['HURRY' , '',  str(self.iSpecialTickCounter) +' Seconds Left!!!'])
          if self.iSpecialTickCounter == 0:
            self.game.sound.fadeout_music()
            self.game.sound.play('miss_shot')
            self.game.sound.play_music('MainAfterMode' +str(self.game.ball) +'_' +str(random.randint(1,3)), loops=5)
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
        self.game.sound.stop('10_seconds')
        self.game.sound.fadeout_music()
        self.game.sound.play('special_hit')
        self.game.sound.play_music('MainAfterMode' +str(self.game.ball) +'_' +str(random.randint(1,3)), loops=5)            
        self.game.score(50000)
        self.game.sound.play('impressive')
        self.game.displayText('Special Awarded', duration = 5)
        self.delay(name='endmode',
            event_type=None,
            delay=1,
            handler=self.endMode)

  def successAdvancePlanetLightShow(self):
    self.game.lamps.pluto.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.neptune.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.uranus.schedule(schedule=0x0000ffff, cycle_seconds=3, now=False)
    self.game.lamps.saturn.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.jupiter.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.mars.schedule(schedule=0x0000ffff, cycle_seconds=3, now=False)
    self.game.lamps.earth.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.venus.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.mercury.schedule(schedule=0x0000ffff, cycle_seconds=3, now=False)

  def SuccessHelper(self):
    self.game.sound.stop('10_seconds')
    self.game.score(50000)
    self.successAdvancePlanetLightShow()
    myList = ['' +self.strPlanetName +' is yours!' , '',  'Hurry to Make Special!']
    self.game.displayText(myList, duration = 5)
    self.bSpecialCountdown = True
    self.game.sound.fadeout_music()
    self.game.sound.play('make_shot')
    self.game.sound.play_music('GetSpecial' +str(self.game.ball))
    self.game.sound.play('special_lit')
    self.delay(name='specialTick',
        event_type=None,
        delay=2,
        handler=self.specialTick)      

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
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_jetMiddle_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_jetBottom_active(self, sw):
      self.checkHit(-1)
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
