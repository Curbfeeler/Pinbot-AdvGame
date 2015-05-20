import procgame.game
import pygame
import my_modes
from pygame.locals import *
from pygame.font import *
from procgame.game import AdvancedMode

class ChestMode(AdvancedMode):

  """
  Example Mode
  """
  def __init__(self, game):
    super(ChestMode, self).__init__(game=game, priority=10, mode_type=AdvancedMode.Ball)
    # stuff that gets done EXACTLY once.
    # happens when the "parent" Game creates this mode
    self.chestFilled = False
    self.chestFilledPoints = 10000
    self.chestFilledDisplayTime = 3
    for switch in self.game.switches:
        if switch.name.find('chestMatrix', 0) != -1:
            self.add_switch_handler(name=switch.name, event_type='active', \
            delay=0.01, handler=self.chestMatrixSwitches)

    ### Chest Matrix Stats ####################################
    self.chestMatrix01={} #YellowRow
    self.chestMatrix01['chestMatrix11']=False
    self.chestMatrix01['chestMatrix12']=False
    self.chestMatrix01['chestMatrix13']=False
    self.chestMatrix01['chestMatrix14']=False
    self.chestMatrix01['chestMatrix15']=False
    self.chestMatrix02={} #BlueRow
    self.chestMatrix02['chestMatrix21']=False
    self.chestMatrix02['chestMatrix22']=False
    self.chestMatrix02['chestMatrix23']=False
    self.chestMatrix02['chestMatrix24']=False
    self.chestMatrix02['chestMatrix25']=False
    self.chestMatrix03={} #OrangeRow
    self.chestMatrix03['chestMatrix31']=False
    self.chestMatrix03['chestMatrix32']=False
    self.chestMatrix03['chestMatrix33']=False
    self.chestMatrix03['chestMatrix34']=False
    self.chestMatrix03['chestMatrix35']=False
    self.chestMatrix04={} #GreenRow
    self.chestMatrix04['chestMatrix41']=False
    self.chestMatrix04['chestMatrix42']=False
    self.chestMatrix04['chestMatrix43']=False
    self.chestMatrix04['chestMatrix44']=False
    self.chestMatrix04['chestMatrix45']=False
    self.chestMatrix05={} #RedRow
    self.chestMatrix05['chestMatrix51']=False
    self.chestMatrix05['chestMatrix52']=False
    self.chestMatrix05['chestMatrix53']=False
    self.chestMatrix05['chestMatrix54']=False
    self.chestMatrix05['chestMatrix55']=False

    self.chestMatrix10={} #YellowCol
    self.chestMatrix10['chestMatrix11']=False
    self.chestMatrix10['chestMatrix21']=False
    self.chestMatrix10['chestMatrix31']=False
    self.chestMatrix10['chestMatrix41']=False
    self.chestMatrix10['chestMatrix51']=False
    self.chestMatrix20={} #BlueCol  
    self.chestMatrix20['chestMatrix12']=False
    self.chestMatrix20['chestMatrix22']=False
    self.chestMatrix20['chestMatrix32']=False
    self.chestMatrix20['chestMatrix42']=False
    self.chestMatrix20['chestMatrix52']=False
    self.chestMatrix30={} #OrangeCol
    self.chestMatrix30['chestMatrix13']=False
    self.chestMatrix30['chestMatrix23']=False
    self.chestMatrix30['chestMatrix33']=False
    self.chestMatrix30['chestMatrix43']=False
    self.chestMatrix30['chestMatrix53']=False
    self.chestMatrix40={} #GreenCol 
    self.chestMatrix40['chestMatrix14']=False
    self.chestMatrix40['chestMatrix24']=False
    self.chestMatrix40['chestMatrix34']=False
    self.chestMatrix40['chestMatrix44']=False
    self.chestMatrix40['chestMatrix54']=False
    self.chestMatrix50={} #RedCol   
    self.chestMatrix50['chestMatrix15']=False
    self.chestMatrix50['chestMatrix25']=False
    self.chestMatrix50['chestMatrix35']=False
    self.chestMatrix50['chestMatrix45']=False
    self.chestMatrix50['chestMatrix55']=False
    
    self.chestRowMatrix = []
    self.chestRowMatrix.append(self.chestMatrix01)
    self.chestRowMatrix.append(self.chestMatrix02)
    self.chestRowMatrix.append(self.chestMatrix03)
    self.chestRowMatrix.append(self.chestMatrix04)
    self.chestRowMatrix.append(self.chestMatrix05)

    self.chestColMatrix = []
    self.chestColMatrix.append(self.chestMatrix10)
    self.chestColMatrix.append(self.chestMatrix20)
    self.chestColMatrix.append(self.chestMatrix30)
    self.chestColMatrix.append(self.chestMatrix40)
    self.chestColMatrix.append(self.chestMatrix50)

    #Switch Denotation
    #chestMatrix01 #Row 0, Col 1, Yellow Switch - Hori
    #chestMatrix02 #Row 0, Col 2, Blue Switch - Hori
    #chestMatrix03 #Row 0, Col 3, Orange Switch - Hori
    #chestMatrix04 #Row 0, Col 4, Green Switch - Hori
    #chestMatrix05 #Row 0, Col 5, Red Switch - Hori
    #chestMatrix10 #Row 1, Col 0, Yellow Switch - Vert
    #chestMatrix20 #Row 2, Col 0, Yellow Switch - Vert
    #chestMatrix30 #Row 3, Col 0, Yellow Switch - Vert
    #chestMatrix40 #Row 4, Col 0, Yellow Switch - Vert
    #chestMatrix50 #Row 5, Col 0, Yellow Switch - Vert
    #    Name            row    col    in code
    #    chestMatrix    1    1    chestMatrix11
    #    chestMatrix    1    2    chestMatrix12
    #    chestMatrix    1    3    chestMatrix13
    #    chestMatrix    1    4    chestMatrix14
    #    chestMatrix    1    5    chestMatrix15
    #    chestMatrix    2    1    chestMatrix21
    #    chestMatrix    2    2    chestMatrix22
    #    chestMatrix    2    3    chestMatrix23
    #    chestMatrix    2    4    chestMatrix24
    #    chestMatrix    2    5    chestMatrix25
    #    chestMatrix    3    1    chestMatrix31
    #    chestMatrix    3    2    chestMatrix32
    #    chestMatrix    3    3    chestMatrix33
    #    chestMatrix    3    4    chestMatrix34
    #    chestMatrix    3    5    chestMatrix35
    #    chestMatrix    4    1    chestMatrix41
    #    chestMatrix    4    2    chestMatrix42
    #    chestMatrix    4    3    chestMatrix43
    #    chestMatrix    4    4    chestMatrix44
    #    chestMatrix    4    5    chestMatrix45
    #    chestMatrix    5    1    chestMatrix51
    #    chestMatrix    5    2    chestMatrix52
    #    chestMatrix    5    3    chestMatrix53
    #    chestMatrix    5    4    chestMatrix54
    #    chestMatrix    5    5    chestMatrix55
    return super(ChestMode, self).mode_started()
  
  def mode_started(self):
    print("My mode started")
    #### Load Mode Feature Defaults ####
    #self.chestHold = self.game.user_settings['Feature']['Chest Hold']
    self.game.displayText("Complete the Chest to Open Visor", duration=4)
    #if (self.chestHold == False):
    self.resetChest()
    #else:
    #    self.update_lamps()    
    pass

  def endMode(self):
    self.game.modes.remove(self)
  
  def mode_stopped(self): 
    print("My mode ended")
    self.game.sound.fadeout_music()
    if self.chestFilled:
        self.game.modes.add(self.game.multiball_mode)
    # do cleanup of the mode here. 


  def update_lamps(self):
    print "update_lamps"
    for num in range(0,4):
        columndatadict = self.chestColMatrix[num]
        for key, value in sorted(columndatadict.items()):
            if value == True:
                self.game.lamps[key].enable()
    pass

  def resetChest(self):
    print "resetChest"
    for num in range(0,4):
        columndatadict = self.chestColMatrix[num]
        for colkey, colvalue in sorted(columndatadict.items()):
            colvalue = False
        rowdatadict = self.chestRowMatrix[num]
        for rowkey, rowvalue in sorted(rowdatadict.items()):
            rowvalue = False
    pass

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


  def chestMade(self, iPoints):
    self.chestFilled = True
    self.game.sound.play('chestMade')
    self.game.displayText("CHEST MADE - " +str(iPoints) +"Points")
    self.game.bonus("CHEST MADE")
    self.game.score(iPoints)

    self.SuccessLightShow()

    self.delay(name='endmode',
        event_type=None,
        delay=1,
        handler=self.endMode)    
    
#     self.game.sound.stop_music()
#     self.game.sound.play_music('MultiB'+ str(self.game.ball),loops=1,music_volume=.5)                
#     self.game.modes.remove(self)
#     self.resetChest()        
#     self.game.modes.add(self.game.multiball_mode)

  def chestMatrixSwitches(self,sw):
    bOneRowKnownComplete = False
    bOneColKnownComplete = False
    self.game.score(100)
    iRowHit = int(sw.name[11])
    iColHit = int(sw.name[12])
    if(iRowHit > 0): #hit a row
        myrowdatadict = self.chestRowMatrix[iRowHit-1]
        iSumDataDict = sum(myrowdatadict.values())
        self.game.displayText("hit row " +str(iRowHit) +":" +str(iSumDataDict+1) +"/5 Made")
        if iSumDataDict==5: #Already all complete!
            pass
        elif iSumDataDict==0: #No rows complete, no reason to "for loop" here 
            self.game.lamps["chestMatrix" +str(iRowHit) +str(iColHit+1)].enable()
            myrowdatadict["chestMatrix" +str(iRowHit) +str(iColHit+1)] = True
            othercoldatadict = self.chestColMatrix[iColHit]
            othercoldatadict["chestMatrix" +str(iRowHit) +str(iColHit+1)] = True
        else:
            for keyA, valueA in sorted(myrowdatadict.items()):
                if valueA == False:
                    self.game.lamps[keyA].enable() #Light same-named lamp
                    myrowdatadict[keyA] = True
                    othercoldatadict = self.chestColMatrix[int(keyA[12])-1]
                    for keyB, valueB in sorted(othercoldatadict.items()):                        
                        if keyB == keyA:
                            othercoldatadict[keyB] = True
                            if iSumDataDict == 4:
                                bOneRowKnownComplete = True
                                self.game.displayText("COL " +str(iColHit) +" MADE!")
                            break
                    break
        #Now check to see if the entire matrix is made            
        if bOneRowKnownComplete and sum(self.chestRowMatrix[4].values())==5 and sum(self.chestRowMatrix[3].values())==5 and sum(self.chestRowMatrix[2].values())==5 and sum(self.chestRowMatrix[1].values())==5 and sum(self.chestRowMatrix[0].values())==5:
            self.chestMade(self.chestFilledPoints)
            pass
    else:            #hit a col
        mycoldatadict = self.chestColMatrix[iColHit-1]
        iSumDataDict = sum(mycoldatadict.values())
        self.game.displayText("hit col " +str(iColHit) +":" +str(iSumDataDict+1) +"/5 Made")
        if iSumDataDict==5: #Already all complete!
            pass
        elif iSumDataDict==0: #No Cols complete, no reason to "for loop" here 
            self.game.lamps["chestMatrix" +str(iRowHit+1) +str(iColHit)].enable()
            mycoldatadict["chestMatrix" +str(iRowHit+1) +str(iColHit)] = True
            otherrowdatadict = self.chestRowMatrix[iRowHit]
            otherrowdatadict["chestMatrix" +str(iColHit) +str(iRowHit+1)] = True
        else:
            for keyA, valueA in sorted(mycoldatadict.items()):
                if valueA == False:
                    self.game.lamps[keyA].enable() #Light same-named lamp
                    mycoldatadict[keyA] = True
                    otherrowdatadict = self.chestRowMatrix[int(keyA[11])-1]
                    for keyB, valueB in sorted(otherrowdatadict.items()):                        
                        if keyB == keyA:
                            otherrowdatadict[keyB] = True
                            if iSumDataDict == 4:
                                bOneColKnownComplete = True
                                self.game.displayText("ROW " +str(iRowHit) +" MADE!")
                            break
                        
                    break
        #Now check to see if the entire matrix is made            
        if bOneColKnownComplete and sum(self.chestColMatrix[4].values())==5 and sum(self.chestColMatrix[3].values())==5 and sum(self.chestColMatrix[2].values())==5 and sum(self.chestColMatrix[1].values())==5 and sum(self.chestColMatrix[0].values())==5:
            self.chestMade(self.chestFilledPoints)
        self.update_lamps()

