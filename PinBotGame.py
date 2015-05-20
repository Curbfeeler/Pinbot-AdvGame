##########################
# this is intended to be a very simple game from which 
# to learn SkeletonGame based PyProcGame programming
#
# The following imports add the "usual" stuff every PyProcGame needs
import logging
import procgame
import procgame.game
import procgame.dmd
from procgame.game import SkeletonGame

from procgame import *
import os

import my_modes
from my_modes import BaseGameMode
from my_modes import SkillShotMode,  EnergyBonusMode, PlanetMode, PlutoMode, NeptuneMode, UranusMode, SaturnMode, JupiterMode, MarsMode, EarthMode, VenusMode, MercuryMode, SolMode, ChestMode, MultiBallMode, MultiplierMode, DropTargetsMode

from procgame.modes import Attract
from procgame.game.skeletongame import run_proc_game

# set up a few more things before we get started 
# the logger's configuration and format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
curr_file_path = os.path.dirname(os.path.abspath( __file__ ))

class PinbotGame(SkeletonGame):

    # constructor for the game object; called once
    def __init__(self):

        # THESE MUST BE DEFINED for SkeletonGame
        self.curr_file_path = curr_file_path
        self.trough_count = 4
        self.lastPlanetVisited = 'None'

        # optional definition for 'auto-closed' switches
        self.osc_closed_switches = ['trough1','trough2''trough3','trough4']

        # call the maker
        # machine yaml must call the:
        #    shooter-feeding coil 'trough'
        #    trough switches numbered left-to-right trough1, trough2, trough3
        #    shooter lane switch 'shooter'
        super(PinbotGame, self).__init__('config/Pinbot.yaml', self.curr_file_path)

        self.base_game_mode = BaseGameMode(game=self)
        self.chest_mode = ChestMode(game=self)
        self.droptargets_mode = DropTargetsMode(game=self)
        self.energybonus_mode = EnergyBonusMode(game=self)
        self.multiplier_mode = MultiplierMode(game=self)
        self.skillshot_mode = SkillShotMode(game=self)

        #Advanced Planet Modes
        self.pluto_mode = PlutoMode(game=self)
        self.neptune_mode = NeptuneMode(game=self)
        self.uranus_mode = UranusMode(game=self)
        self.saturn_mode = SaturnMode(game=self)
        self.jupiter_mode = JupiterMode(game=self)
        self.mars_mode = MarsMode(game=self)
        self.earth_mode = EarthMode(game=self)
        self.venus_mode = VenusMode(game=self)
        self.mercury_mode = MercuryMode(game=self)
        self.sol_mode = SolMode(game=self)

        # call reset (to reset the machine/modes/etc)
        self.reset()

    # called when you want to fully reset the game
    def reset(self):
        # EVERY SkeletonGame game should start its reset() with a call to super()
        super(PinbotGame,self).reset()

        # try to set the game up to be in a clean state from the outset:
        self.doBallSearch()
        
        # initialize the mode variables; the general form is:
        # self.varName = fileName.classModeName(game=self)
        # Note this creates the mode and causes the Mode's constructor
        # function --aka __init__()  to be run
        # self.some_non_advancedMode = ModeFile.MyMode(game=self)

        # add /some/ of the modes to the game's mode queue: 
        # as soon as you add a mode, it is active/starts.
        # modes added here

        # EVERY SkeletonGame game should end its reset() with a call to start_attract_mode()
        self.start_attract_mode() # plays the attract mode and kicks off the game
        
    def lanes(self):
        """ TODO: replace-me with a better example """
        print("ALL THREE")


    # function that is called whenever a ball starts
    # You should NOT need ANY of these

    # def start_ball(self):
    #     super(T2Game, self).start_ball()

    # def start_game(self):
    #     """ called (by attract) when the game is starting """
    #     super(T2Game,self).start_game()

    # def ball_starting(self):
    #     """ this is auto-called when the ball is actually starting 
    #         (so happens 3 or more times a game) """

    # def ball_ended(self):
    #     """ Called by end_ball(). At this point the ball is over """
    #     super(T2Game, self).ball_ended()

    # def game_ended(self):
    #     super(T2Game, self).game_ended()

    def doBallSearch(self):
        # try to set the game up to be in a clean state from the outset:
        if(self.switches.outhole.is_active()):
            self.coils.outholeKicker_Knocker.pulse()
        if(self.switches.leftEyeball.is_active()):
            self.coils.leftEyeballEject_LeftPlayfieldFlasher.pulse()
        if(self.switches.rightEyeball.is_active()):
            self.coils.rightEyeballEject_SunFlasher.pulse()
        if(self.switches.singleEject.is_active()):
            self.coils.singleEjectHole_LeftInsertBDFlasher.pulse()

## the following just set things up such that you can run Python ExampleGame.py
# and it will create an instance of the correct game objct and start running it!

if __name__ == '__main__':
    # change T2Game to be the class defined in this file!
    run_proc_game(PinbotGame)
