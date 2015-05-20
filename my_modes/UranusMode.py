import procgame.game
import pygame
import my_modes
import random
from pygame.locals import *
from pygame.font import *
from my_modes import PlanetMode

class UranusMode(PlanetMode):
  """
  This is the skillshot- it lights the sequence of lights and
  registers hits on the targets on the left hand side.
  """
  def __init__(self, game):
    super(PlanetMode, self).__init__(game=game, priority=40)
    self.iPlanetTickCounter = 120
    self.arrRow2Swx = [0]*5
    self.arrRow4Swx = [0]*5
    self.arrCol2Swx = [0]*5
    self.arrCol4Swx = [0]*5
    self.iSpecialTickCounter = 60
    self.bSpecialCountdown = False
    self.strPlanetVoice = 'uranus_bluegreen'
    self.strPlanetName = 'Uranus'
    self.strPlanetDisplayText = ['Welcome to Uranus', '', 'Light All Blue and Green Rows and Cols']
    pass

  def checkHit(self, num):
      if(num == -1):
          self.game.sound.play('target')
          self.game.score(100)
      else:
          self.game.sound.play('target')
          self.game.score(1000)
          iCount = 0
          iChanges = 0
    
          if num == 20:
              while(sum(self.arrRow2Swx)<5 and iChanges==False):
                  if self.arrRow2Swx[iCount] == 0:
                      self.arrRow2Swx[iCount] = 1
                      iChanges = True
                  iCount = iCount + 1                         
          elif num == 40:
              while(sum(self.arrRow4Swx)<5 and iChanges==False):
                  if self.arrRow4Swx[iCount] == 0:
                      self.arrRow4Swx[iCount] = 1
                      iChanges = True
                  iCount = iCount + 1                         
          elif num == 2:
              while(sum(self.arrCol2Swx)<5 and iChanges==False):
                  if self.arrCol2Swx[iCount] == 0:
                      self.arrCol2Swx[iCount] = 1
                      iChanges = True
                  iCount = iCount + 1                         
          elif num == 4:
              while(sum(self.arrCol4Swx)<5 and iChanges==False):
                  if self.arrCol4Swx[iCount] == 0:
                      self.arrCol4Swx[iCount] = 1
                      iChanges = True
                  iCount = iCount + 1
          self.updateModeLamps()
          if(sum(self.arrRow2Swx) + sum(self.arrRow4Swx) + sum(self.arrCol2Swx) + sum(self.arrCol4Swx)) == 20:
            self.SuccessHelper()




  def updateModeLamps(self):
    #Row 2 including shared spaces
    if self.arrRow2Swx[0] == 1:
        self.game.lamps.chestMatrix21.enable()

    if self.arrRow2Swx[1] + self.arrCol2Swx[1] == 2:
        self.game.lamps.chestMatrix22.enable()
    if self.arrRow2Swx[1] + self.arrCol2Swx[1] == 1:
        self.game.lamps.chestMatrix22.schedule(schedule=0x00000fc0, cycle_seconds=0, now=False)

    if self.arrRow2Swx[2] == 1:
        self.game.lamps.chestMatrix23.enable()

    if self.arrRow2Swx[3] + self.arrCol2Swx[3] == 2:
        self.game.lamps.chestMatrix24.enable()
    if self.arrRow2Swx[3] + self.arrCol2Swx[3] == 1:
        self.game.lamps.chestMatrix24.schedule(schedule=0x00000fc0, cycle_seconds=0, now=False)

    if self.arrRow2Swx[4] == 1:
        self.game.lamps.chestMatrix25.enable()

    #Row 4 including shared spaces
    if self.arrRow4Swx[0] == 1:
        self.game.lamps.chestMatrix41.enable()

    if self.arrRow4Swx[1] + self.arrCol4Swx[1] == 2:
        self.game.lamps.chestMatrix42.enable()
    if self.arrRow4Swx[1] + self.arrCol4Swx[1] == 1:
        self.game.lamps.chestMatrix42.schedule(schedule=0x00000fc0, cycle_seconds=0, now=False)

    if self.arrRow4Swx[2] == 1:
        self.game.lamps.chestMatrix43.enable()

    if self.arrRow4Swx[3] + self.arrCol4Swx[3] == 2:
        self.game.lamps.chestMatrix44.enable()
    if self.arrRow4Swx[3] + self.arrCol4Swx[3] == 1:
        self.game.lamps.chestMatrix44.schedule(schedule=0x00000fc0, cycle_seconds=0, now=False)

    if self.arrRow4Swx[4] == 1:
        self.game.lamps.chestMatrix45.enable()

#Col 2
    if self.arrCol2Swx[0] == 1:
        self.game.lamps.chestMatrix12.enable()

    if self.arrCol2Swx[2] == 1:
        self.game.lamps.chestMatrix32.enable()

    if self.arrCol2Swx[4] == 1:
        self.game.lamps.chestMatrix52.enable()

#Col4
    if self.arrCol4Swx[0] == 1:
        self.game.lamps.chestMatrix14.enable()

    if self.arrCol4Swx[2] == 1:
        self.game.lamps.chestMatrix34.enable()

    if self.arrCol4Swx[4] == 1:
        self.game.lamps.chestMatrix54.enable()

  def disableModeLamps(self):
    self.game.lamps.chestMatrix11.disable()
    self.game.lamps.chestMatrix12.disable()
    self.game.lamps.chestMatrix13.disable()
    self.game.lamps.chestMatrix14.disable()
    self.game.lamps.chestMatrix15.disable()

    self.game.lamps.chestMatrix21.disable()
    self.game.lamps.chestMatrix22.disable()
    self.game.lamps.chestMatrix23.disable()
    self.game.lamps.chestMatrix24.disable()
    self.game.lamps.chestMatrix25.disable()

    self.game.lamps.chestMatrix31.disable()
    self.game.lamps.chestMatrix32.disable()
    self.game.lamps.chestMatrix33.disable()
    self.game.lamps.chestMatrix34.disable()
    self.game.lamps.chestMatrix35.disable()

    self.game.lamps.chestMatrix41.disable()
    self.game.lamps.chestMatrix42.disable()
    self.game.lamps.chestMatrix43.disable()
    self.game.lamps.chestMatrix44.disable()
    self.game.lamps.chestMatrix45.disable()

    self.game.lamps.chestMatrix51.disable()
    self.game.lamps.chestMatrix52.disable()
    self.game.lamps.chestMatrix53.disable()
    self.game.lamps.chestMatrix54.disable()
    self.game.lamps.chestMatrix55.disable()

  def sw_chestMatrix02_active(self, sw):
      self.checkHit(2)
      return procgame.game.SwitchStop

  def sw_chestMatrix04_active(self, sw):
      self.checkHit(4)
      return procgame.game.SwitchStop

  def sw_chestMatrix20_active(self, sw):
      self.checkHit(20)
      return procgame.game.SwitchStop
  
  def sw_chestMatrix40_active(self, sw):
      self.checkHit(40)
      return procgame.game.SwitchStop

