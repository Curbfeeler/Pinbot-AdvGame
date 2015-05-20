import procgame.game
import pygame
import random
from pygame.locals import *
from pygame.font import *
from procgame.game import AdvancedMode

class SkillShotMode(AdvancedMode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(SkillShotMode, self).__init__(game=game, priority=11, mode_type=AdvancedMode.Ball)
    self.game.droptargets_mode.EnergyTickActive = False
    self.currentTarget = 1
    self.lastTarget = 1
    self.shotnum = 0
    self.direction = 1
    self.speeds = [1.3, 1.1, 1.0]
    self.awards = [200000, 225000, 250000]
    self.targets = [self.game.switches.chestMatrix05,
                    self.game.switches.chestMatrix04,
                    self.game.switches.chestMatrix03,
                    self.game.switches.chestMatrix02,
                    self.game.switches.chestMatrix01,
                    self.game.switches.chestMatrix10,
                    self.game.switches.chestMatrix20,
                    self.game.switches.chestMatrix30,
                    self.game.switches.chestMatrix40,
                    self.game.switches.chestMatrix50]
    self.lights = [ self.game.lamps.chestMatrix11,
                    self.game.lamps.chestMatrix12,
                    self.game.lamps.chestMatrix13,
                    self.game.lamps.chestMatrix14,
                    self.game.lamps.chestMatrix15,
                    self.game.lamps.chestMatrix15,
                    self.game.lamps.chestMatrix25,
                    self.game.lamps.chestMatrix35,
                    self.game.lamps.chestMatrix45,
                    self.game.lamps.chestMatrix55]
    self.finishingUp = False
    pass

  def mode_started(self):
    self.finishingUp = False
    print("SS: skill shot mode began.")
    self.game.sound.play_music('Main' +str(self.game.ball))
    list1 = [' ', 'Shoot VORTEX', 'or hit chaser', 'for SUPER BONUS', ' ']
    #mode.layer = dmd.MovieLayer( opaque=True, hold=False, repeat=True, frame_time=1, movie=dmd.Movie().load(game.dmd_path+'stars.mp4'))
    self.game.displayText(msg = list1, duration = 8, background_layer = 'starsgif')
    self.game.droptargets_mode.EnergyTickActive = False
    self.ssTick()

  def endMode(self):
    self.game.modes.remove(self)

  def ssTick(self):
    self.game.sound.play('ss_tick')
    self.lastTarget = self.currentTarget
    self.currentTarget = self.currentTarget + self.direction
    if(self.currentTarget == 1):
      self.direction = 1
    elif(self.currentTarget == 10):
      self.direction = -1
    print("SS: aim for: " + str(self.currentTarget))
    self.lights[self.lastTarget - 1].disable()
    self.lights[self.currentTarget - 1].enable()
    self.delay(name='ssTick',
            event_type=None,
            delay=self.speeds[self.shotnum],
            handler=self.ssTick)

  def mode_stopped(self):  # naming is inconsistent with game_ended/ball_ended
    self.game.lamps.chestMatrix11.disable()
    self.game.lamps.chestMatrix12.disable()
    self.game.lamps.chestMatrix13.disable()
    self.game.lamps.chestMatrix14.disable()
    self.game.lamps.chestMatrix15.disable()
    self.game.lamps.chestMatrix25.disable()
    self.game.lamps.chestMatrix35.disable()
    self.game.lamps.chestMatrix45.disable()
    self.game.lamps.chestMatrix55.disable()
    self.game.droptargets_mode.EnergyTickActive = True
    self.game.droptargets_mode.dtEnergyTick()
    self.game.droptargets_mode.dtAdvPlanentTick()
    self.game.sound.play_music('MainAfterMode' +str(self.game.ball) +'_' +str(random.randint(2,3)), loops=5)

    print("SS: skill shot mode complete.")


  def checkHit(self, num):
    if(self.finishingUp == True):
      return

    self.finishingUp = True
    self.cancel_delayed(name='ssTick')
    if(self.currentTarget == num):
      self.game.sound.fadeout_music()      
      self.game.sound.play('wow')
      self.game.displayText("Direct Hit!!", 'explosion')
      self.game.bonus("DIRECT HIT")
      self.game.score(self.awards[self.shotnum])
      self.shotnum = self.shotnum + 1

      if(self.shotnum >= len(self.awards)):
        self.shotnum = len(self.awards) - 1
      self.SuccessLightShow()

    else:
      self.game.sound.fadeout_music()      
      self.game.sound.play('wah_wah')
      self.game.displayText("better luck next time!")
    self.delay(name='endmode',
        event_type=None,
        delay=1,
        handler=self.endMode)

  def vortexMade(self, iPoints):
    self.game.sound.play('wow')
    self.game.sound.fadeout_music()    
    self.game.displayText("Vortex " +str(iPoints))
    self.game.bonus("VORTEX MADE")
    self.game.score(iPoints)
    self.SuccessLightShow()

    self.delay(name='endmode',
        event_type=None,
        delay=1,
        handler=self.endMode)


  def SuccessLightShow(self):
    # play a little light show for the successful hit
    self.game.lamps.chestMatrix11.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.chestMatrix12.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.chestMatrix13.schedule(schedule=0x0000ffff, cycle_seconds=3, now=False)
    self.game.lamps.chestMatrix14.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.chestMatrix15.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.chestMatrix11.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.chestMatrix12.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.chestMatrix13.schedule(schedule=0x0000ffff, cycle_seconds=3, now=False)
    self.game.lamps.chestMatrix14.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.chestMatrix15.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)

###########################
## Switch Handling Modes ##
###########################


  def sw_vortex5k_active(self, sw):
      self.vortexMade(5000)
      return procgame.game.SwitchContinue

  def sw_vortex20k_active(self, sw):
      self.vortexMade(20000)
      return procgame.game.SwitchContinue

  def sw_vortex100k_active(self, sw):
      self.vortexMade(100000)
      return procgame.game.SwitchContinue
  
  def sw_chestMatrix01_active(self, sw):
      self.checkHit(1)
      return procgame.game.SwitchStop
  
  def sw_chestMatrix02_active(self, sw):
      self.checkHit(2)
      return procgame.game.SwitchStop

  def sw_chestMatrix03_active(self, sw):
      self.checkHit(3)
      return procgame.game.SwitchStop

  def sw_chestMatrix04_active(self, sw):
      self.checkHit(4)
      return procgame.game.SwitchStop

  def sw_chestMatrix05_active(self, sw):
      self.checkHit(5)
      return procgame.game.SwitchStop

  def sw_chestMatrix10_active(self, sw):
      self.checkHit(10)
      return procgame.game.SwitchStop

  def sw_chestMatrix20_active(self, sw):
      self.checkHit(20)
      return procgame.game.SwitchStop
  
  def sw_chestMatrix30_active(self, sw):
      self.checkHit(30)
      return procgame.game.SwitchStop
  
  def sw_chestMatrix40_active(self, sw):
      self.checkHit(40)
      return procgame.game.SwitchStop
  
  def sw_chestMatrix50_active(self, sw):
      self.checkHit(50)
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
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_tenPointer3_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_upperDrop_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_midDrop_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_lowerDrop_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_scoreEnergyStandUp_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop

  def sw_advancePlanent_active(self, sw):
      self.checkHit(-1)
      return procgame.game.SwitchStop
