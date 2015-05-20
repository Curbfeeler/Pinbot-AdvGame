import procgame.game
from procgame.game import AdvancedMode

import pygame
from pygame.locals import *
from pygame.font import *

class BaseGameMode(procgame.game.AdvancedMode):
    """
    A mode that runs whenever the GAME is in progress.
    (notice the super() function call specifies type .Game)
    - it is automatically added when a game starts
        (mode_started will be called once per game)
    - it is automatically removed when a game ends
        (mode_stopped will be called once per game)

    NOTE: a second player does not cause a second game
        (confusing, no doubt).  When a new player is
        added, an evt_player_added will fire.  When
        a new ball starts, that's a good time to ensure
        our data comes from that player and sync up
        lamps via a call to update_lamps.  Read on...
    """

    def __init__(self, game):
        """ 
        The __init__ function is called automatically whenever an instance 
        of this object is created --e.g., whenever the code:
                something = new BaseGameMode() 
        is executed, this __init__ function is called
        """

        # a call to 'super' call's the parent object's __init__ method
        # in this case, it calls the procgame.game.Mode's init()
        super(BaseGameMode, self).__init__(game=game, priority=5, mode_type=AdvancedMode.Game)

        # You might be used to storing data, right in the mode, like as follows:
        # self.multiplier = 0
        # self.standupSwitchL = False
        # self.standupSwitchC = False
        # self.standupSwitchR = False
        # self.idle_balls = 0
        # self.leftTargets = [False, False, False, False, False]
        # self.kickbackEnabled = False

        # but these are properties of the PLAYER not the mode, so we
        # store them there, instead, when the player is added to the game!

    def evt_player_added(self, player):
        player.setState('multiplier', 0)
        player.setState('idle_balls', 0)


    def evt_ball_starting(self):
        # to use the ball saver, we give it the name of a ball-saver
        # method to be called when the ball is saved --that is 
        # defined below
        self.game.ball_saver_enable(num_balls_to_save=1, time=20, now=True, 
            allow_multiple_saves=False, callback=self.ballsaved)


    def ballsaved(self):
        """ this is the method that we told the ball-saver to call if
            the ball is saved by the ball-saver; see the call to 
            ball_saver_enable.  This just shows a message and plays a
            sound but does NOT launch balls.  The ballsaver/trough
            handle this for us!
        """
        self.game.log("BaseGameMode: BALL SAVED from Trough callback")
        self.game.sound.play('ball_saved')
        self.game.displayText('Ball Saved!')
        self.game.coils.top4CenterFlashers.pulse()
        # Do NOT tell the trough to launch balls!  It's handled automatically!
        # self.game.trough.launch_balls(1)

    def mode_started(self):
        """
        the mode_started method is called whenever this mode is added
        to the mode queue; this might happen multiple times per game,
        depending on how the Game itself adds/removes it.  B/C this is 
        an advancedMode, we know when it will be added/removed.
        """

    def mode_stopped(self): 
        """
        the mode_stopped method is called whenever this mode is removed
        from the mode queue; this might happen multiple times per game,
        depending on how the Game itself adds/removes it
        """
        pass

    def update_lamps(self):
        """ 
        update_lamps is a very important method -- you use it to set the lamps
        to reflect the current state of the internal mode progress variables.
        This function is called after a lampshow is played so that the state
        variables are correct after the lampshow is done.  It's also used other
        times.

        Notice that progress is stored in the player object, so check with:
            self.game.getPlayerState(key)
        which is a wrapper around:
            self.game.get_current_player().getState(key)
        """

        if(self.game.getPlayerState('multiplier') == 2):
            self.game.lamps.x2Bonus.enable()
        else:
            self.game.lamps.x2Bonus.disable()
        if(self.game.getPlayerState('multiplier') == 3):
            self.game.lamps.x3Bonus.enable()
        else:
            self.game.lamps.x3Bonus.disable()
        if(self.game.getPlayerState('multiplier') == 4):
            self.game.lamps.x4Bonus.enable()
        else:
            self.game.lamps.x4Bonus.disable()
        if(self.game.getPlayerState('multiplier') == 5):
            self.game.lamps.x5Bonus.enable()
        else:
            self.game.lamps.x5Bonus.disable()

         # standupMid target states
        if(self.game.getPlayerState('standupSwitchL')):
            self.game.lamps.standupMidL.enable()
        else:
            self.game.lamps.standupMidL.disable()

        if(self.game.getPlayerState('standupSwitchC')): 
            self.game.lamps.standupMidC.enable()
        else:
            self.game.lamps.standupMidC.disable()

        if(self.game.getPlayerState('standupSwitchR')): 
            self.game.lamps.standupMidR.enable()
        else:
            self.game.lamps.standupMidR.disable()

        # here's an example of using an array (list) of lamps
        # defined in the game (look at T2Game's __init__ method)
        # and an array of player states to make quick work of syncing
        # several lamps to target states:
        leftTargetStates = self.game.getPlayerState('leftTargets')

        for target,lamp in zip(leftTargetStates,self.game.leftTargetLamps):
            if(target):
                lamp.enable()
            else:
                lamp.disable()                        

    """ The following are the event handlers for events broadcast by SkeletonGame.  
        handling these events lets your mode give custom feedback to the player
        (lamps, dmd, sound, etc)
    """

    def evt_ball_ending(self, (shoot_again, last_ball)):
        """ this is the handler for the evt_ball_ending event.  It shows    
            the player information about the specific event.  You can optionally
            return a number, which is the number of seconds that you are requesting
            to delay the commitment of the event.  For example, if I wanted to show
            a message for 5 seconds before the ball actually ended (and bonus mode
            began), I would return 5.  Returning 0 (or None) would indicate no delay.
        """
        self.game.log("base game mode trough changed notification ('ball_ending - again=%s, last=%s')" % (shoot_again,last_ball))

        # stop any music as appropriate
        self.game.sound.fadeout_music()

        self.game.sound.play('ball_drain')
        self.game.displayText('BGM Ball Ended!')
        return 2.0

    def evt_game_ending(self):
        self.game.log("base game mode game changed notification ('game_ending')")

        self.game.displayText("GAME ENDED", 'gameover')

        # Do NOT call game_ended any more!!!!!
        # not now or later!

        return 2


    """
    this is an example of a timed switch handler
         sw_      : indicates a switch handler
         outhole  : the name of the switch
         active   : the state (could be inactive, open, closed)
         for_200ms: how long that the switch must be detected
                                in this state before this handler is called

    in this case, if the controller sees this switch closed
    for 200ms, then this function is called; waiting 200ms
    will wait for long enough for the ball to settle in the
    slot before responding
    """
    def sw_outhole_active_for_200ms(self,sw):
            self.game.coils.outholeKicker_Knocker.pulse()
        

    """ The following methods illustrate handling a bank of related
        targets.  Notice that the logical state of the switch is 
        stored in the player's object.  Each of these functions
        are VERY similar, and that might be annoying to you
        (and should be).  An example of a 'better way' follows these.
    """


    def sw_slingL_active(self, sw):
        self.game.score(100)
        self.game.sound.play('sling')
        return procgame.game.SwitchContinue

    def sw_slingR_active(self, sw):
        self.game.score(100)
        self.game.sound.play('sling')
        return procgame.game.SwitchContinue

