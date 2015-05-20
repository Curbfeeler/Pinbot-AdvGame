import procgame.game
import pygame
import my_modes
from pygame.locals import *
from pygame.font import *
from procgame.game import AdvancedMode

class DropTargetsMode(AdvancedMode):
  """
  This is the droptargets- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(DropTargetsMode, self).__init__(game=game, priority=10, mode_type=AdvancedMode.Ball)
    self.rampUpCounter = 1
    self.advancePlanetCounter = 1
    self.currentTarget = 1
    self.lastTarget = 1
    self.shotnum = 0
    self.direction = 1
    self.bForceAdvancePlanetEnd = False
    self.speeds = [1.3, 1.1, 1.0]
    self.awards = [200000, 225000, 250000]
    self.targets = [self.game.switches.upperDrop,
                    self.game.switches.midDrop,
                    self.game.switches.lowerDrop]
    self.lights = [ self.game.lamps.dropTarget1Top,
                    self.game.lamps.dropTarget2Middle,
                    self.game.lamps.dropTarget3Bottom]
    self.finishingUp = False
    self.rampUp = False
    self.advancePlanetActive = False
    self.bForcerampDown = False
    self.EnergyTickActive = True
    pass

  def mode_started(self):
    self.finishingUp = False
    self.advancePlanetActive = False
    print("droptargets mode began.")
    self.dtAdvPlanentTick()
    self.dtEnergyTick()

  def endMode(self):
    self.game.modes.remove(self)

  def mode_stopped(self):  # naming is inconsistent with game_ended/ball_ended
    self.game.lamps.dropTarget1Top.disable()
    self.game.lamps.dropTarget2Middle.disable()
    self.game.lamps.dropTarget3Bottom.disable()
    self.game.lamps.scoreEnergy.disable()
    self.game.lamps.dropTargetTimerLamp.disable()
    self.game.lamps.advancePlanent.disable()   
    #if(self.game.switches.upperDrop.state == True or self.game.switches.midDrop.state == True or self.game.switches.lowerDrop.state == True):
    self.game.coils.dropTargetReset_RightInsertBDFlasher.pulse(150)
    #if(self.game.switches.rampIsDown.state == False):
    self.lowerRamp()
    self.advancePlanetActive = False    

    print("droptargets mode complete.")

  def dtAdvPlanentTick(self):
    if self.EnergyTickActive == True:
        if self.advancePlanetActive == True:
            self.game.displayText("Advance Planet Lit ... " +str(30-self.advancePlanetCounter), duration = 1) 
            self.game.lamps.advancePlanent.enable()
            self.advancePlanetCounter = self.advancePlanetCounter + 1
            if self.advancePlanetCounter == 30 or self.bForceAdvancePlanetEnd == True:
                self.game.coils.dropTargetReset_RightInsertBDFlasher.pulse(150)            
                self.advancePlanetCounter = 1
                self.advancePlanetActive = False
        else:
            self.game.lamps.advancePlanent.disable()
        self.delay(name='dtAdvPlanentTick',
                event_type=None,
                delay=self.speeds[self.shotnum],
                handler=self.dtAdvPlanentTick)
    else:
        self.game.lamps.dropTarget1Top.disable()
        self.game.lamps.dropTarget2Middle.disable()
        self.game.lamps.dropTarget3Bottom.disable()
        self.game.lamps.scoreEnergy.disable()
        self.game.lamps.dropTargetTimerLamp.disable()
        self.game.lamps.advancePlanent.disable()
        pass

  def dtEnergyTick(self):
    if self.EnergyTickActive == True:
        if self.rampUp == True:
            if self.rampUpCounter % 2 == 0:
                self.game.lamps.scoreEnergy.enable()
                self.game.lamps.dropTargetTimerLamp.disable()
            else:
                self.game.lamps.scoreEnergy.disable()
                self.game.lamps.dropTargetTimerLamp.enable()
    
            self.rampUpCounter = self.rampUpCounter + 1
    
            if self.rampUpCounter == 10 or self.bForcerampDown == True:
                self.rampUpCounter = 1
                self.rampUp = False
                self.delay(name='dtLowerRamp',
                    event_type=None,
                    delay=self.speeds[self.shotnum],
                    handler=self.lowerRamp)
                self.game.coils.dropTargetReset_RightInsertBDFlasher.pulse(150)
                self.game.lamps.scoreEnergy.disable()
                self.game.lamps.dropTargetTimerLamp.disable()
                self.bForcerampDown = False
                self.finishingUp = False
            self.delay(name='dtEnergyTick',
            event_type=None,
            delay=self.speeds[self.shotnum],
            handler=self.dtEnergyTick)
            pass
        else:
            self.lastTarget = self.currentTarget
            self.currentTarget = self.currentTarget + self.direction
            if(self.currentTarget == 1):
              self.direction = 1
            elif(self.currentTarget == 3):
              self.direction = -1
            print("DT: aim for: " + str(self.currentTarget))
            self.lights[self.lastTarget - 1].disable()
            self.lights[self.currentTarget - 1].enable()
            self.delay(name='dtEnergyTick',
                    event_type=None,
                    delay=self.speeds[self.shotnum],
                    handler=self.dtEnergyTick)
    else:
        self.lowerRamp()
        self.game.lamps.dropTarget1Top.disable()
        self.game.lamps.dropTarget2Middle.disable()
        self.game.lamps.dropTarget3Bottom.disable()
        self.game.lamps.scoreEnergy.disable()
        self.game.lamps.dropTargetTimerLamp.disable()
        self.game.lamps.advancePlanent.disable()
        pass
    
  def lowerRamp(self):
      self.game.lamps.scoreEnergy.disable()      
      self.game.coils.lowerRamp_EnergyFlashers.pulse(100)

  def checkEnergyHit(self, num):
    if(self.finishingUp == True):
      self.game.displayText("finishingUp!", duration = 2) 
      return

    self.finishingUp = True
    self.cancel_delayed(name='droptargets')
            
    if(self.currentTarget == num):
        self.game.coils.raiseRamp_LowerPFTop1Flasher.pulse(100)
        self.game.lamps.dropTarget1Top.disable()
        self.game.lamps.dropTarget2Middle.disable()
        self.game.lamps.dropTarget3Bottom.disable()
        self.rampUp = True
    else:
        self.finishingUp = False
        pass

  def checkAdvPlanetHit(self):
    if(self.game.switches.upperDrop.state == True and self.game.switches.midDrop.state == True and self.game.switches.lowerDrop.state == True):
        self.game.displayText("GOT ALL THREE DROPS!", duration = 3) 
        self.advancePlanetActive = True

  def SuccessDropLightShow(self):
    # play a little light show for the successful hit
    self.game.lamps.dropTarget1Top.schedule(schedule=0xffc0000c, cycle_seconds=3, now=False)
    self.game.lamps.dropTarget2Middle.schedule(schedule=0x00ffc00c, cycle_seconds=3, now=False)
    self.game.lamps.dropTarget3Bottom.schedule(schedule=0x0000ffff, cycle_seconds=3, now=False)

     
  def startNextPlanet(self, strPreviousPlanet):
    self.game.sound.fadeout_music()
    self.game.sound.play('make_shot')
    
    if strPreviousPlanet == 'None':
      self.game.lamps.pluto.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.pluto_mode)
    elif strPreviousPlanet == 'Pluto':
      self.game.lamps.neptune.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.neptune_mode)
    elif strPreviousPlanet == 'Neptune':
      self.game.lamps.saturn.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.uranus_mode)
    elif strPreviousPlanet == 'Uranus':
      self.game.lamps.saturn.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.saturn_mode)
    elif strPreviousPlanet == 'Saturn':
      self.game.lamps.saturn.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.jupiter_mode)
    elif strPreviousPlanet == 'Jupiter':
      self.game.lamps.saturn.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.mars_mode)
    elif strPreviousPlanet == 'Mars':
      self.game.lamps.saturn.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.earth_mode)
    elif strPreviousPlanet == 'Earth':
      self.game.lamps.saturn.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.venus_mode)
    elif strPreviousPlanet == 'Venus':
      self.game.lamps.saturn.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.mercury_mode)
    elif strPreviousPlanet == 'Mercury':
      self.game.lamps.saturn.schedule(schedule=0xff00ff00, cycle_seconds=30, now=False)
      self.game.modes.add(self.game.sol_mode)
    
###########################
## Switch Handling Modes ##
###########################

  
  def sw_upperDrop_active(self, sw):
      self.checkEnergyHit(1)
      self.checkAdvPlanetHit()
      return procgame.game.SwitchStop
  
  def sw_midDrop_active(self, sw):
      self.checkEnergyHit(2)
      self.checkAdvPlanetHit()
      return procgame.game.SwitchStop

  def sw_lowerDrop_active(self, sw):
      self.checkEnergyHit(3)
      self.checkAdvPlanetHit()
      return procgame.game.SwitchStop

  def sw_scoreEnergyStandUp_active(self, sw):
    if self.rampUp == True:
        list1 = [' ', 'SCORE ENERGY BONUS', '', str(self.game.energybonus_mode.energyBonus), ' ']
        self.game.displayText(msg = list1, duration = 3) 
        self.game.score(self.game.energybonus_mode.energyBonus)
        self.game.energybonus_mode.energyBonus = 0
        self.bForcerampDown = True
        return procgame.game.SwitchStop

  def sw_advancePlanent_active(self, sw):
       if(self.advancePlanetActive == True):
           #self.startNextPlanet(self.game.getPlayerState(self, key='lastPlanetVisited'))
           self.advancePlanetActive = False
           self.startNextPlanet(self.game.lastPlanetVisited)
           #self.SuccessAdvancePlanetLightShow()
           #self.game.displayText("WooHoo!", duration = 3) 
       pass



  def sw_tenPointer2_BehindDropBank_active(self, sw):
      pass
      #return procgame.game.SwitchStop
