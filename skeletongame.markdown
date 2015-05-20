# SkeletonGame #


    SkeletonGame        (L3)
    ------------------------
    BasicGame           (L2)
    ------------------------
    libpinproc/pinproc  (L1)
    ------------------------


SkeletonGame" --it's a proper third tier on top of BasicGame; think of it as the logical continuation of Starter.py --that is, if starter were a class that people were expected to subclass.  SkeletonGame is just a bunch of additions to  pyprocgame. It leverages everything that those of use who use PyProcGame know and love, and only intends to streamline some things for new users. It should help you make games faster.  Think of it as sucking out the best parts of the Judge Dredd sample game, modifying it to be generic, running on top of HD VGA, and then adding stuff to make games easier.

Motivation: Most people who learn PyProcGame programming have done so by looking at existing open-source games and there are many good ones to learn from.  Unfortunately, the copy/paste/merge process is fairly error prone. I've done it a few times now and it gets dangerous with sequence dependant, asynchronous (i.e., event-driven) code that spans multiple files. Suppose 'project A' assumes that the attract mode will call `start_ball()`, but 'project B' assumes that `start_ball()` is called by the trough handler --depending on what you grab and from where, you may wind up with no balls in the trough or two balls.  Worse I've seen and encountered plenty of instances of the game appearing to be hung or crashing because some event doesn't occur due to functions being called in the wrong order as a result of copy/paste/merge-fail. Having worked on a few P-ROC projects now, I've tried to distill the common bits from each of those games so that I can avoid rewriting the same lines again and again.

## Goals: ##
If SkeletonGame works, it means you (as the programmer) should:

- have VERY few lines of code in your game class.
- spend most of your time coding the logic for *modes*.
- be able to leverage fairly standard modes that have been written before.
- use helpers to create DMD content (in code) much easier.
- get started quickly.


#### SkeletonGame includes: ####

- SkeletonGame is a subclass of `BasicGame`.  This class will serve as the new superclass for people's games. This class includes the following (by default):
    - tracking ball counts, ball time, game counts, game time, loads/saves settings and data
    - assetManager (all your images, sounds, music, fonts, lampshows are pre-loaded by defining a yaml file)
    - a better `Player` class: supports player state tracking built in with appropriate methods for access. 
    - `soundController` mode auto created and loaded 
    - OSC mode auto loaded (though apparently based on an old version..oops)
    - Built-in (already working) trough and ballsave management (both based on Adam's)
    -  ... a VERY simple attract mode that's based on a simple, yet powerful yaml file/format
    -  ... service mode (basically Adam's) that senses dmd size
    -  ... high score entry (based on Adam's but in color) that senses dmd size
    -  ... high score frame generation for display in attract mode
    -  ... score display essentially based on Adam's but updated to use color fonts, background animations, etc. 
    -  ... bonus helper (just like score: `bonus(tag, quantity)`) and a built-in bonus tally mode that kicks in at the end of the ball and shows any bonuses awarded to the player during their ball
    - a Tilt mode that monitors the plumb tilt and the slam tilt switches (which must be named `tilt` and `slamTilt` respectively) -- when tilted all non-trough switches are blocked until all balls are returned to the trough
- `dmdHelper` "mode" that generates a message on screen shown over a single image/animation, or a stack of them. It makes using the DMD extremely painless.  It's usage is: ```displayText(text, key)``` 
If key is a list, it builds a grouped layer for all the keys. If text is a list instead of single string, all the text is shown on the frame. A single line is centered vertically, two lines are shown at 1/3, and 2/3, three lines at 1/4,2/4, and 3/4... You get the idea. 
- Automatic state progressions without having to code for it in your game.  No more calls to `start_ball()`, `end_ball()`, etc.  
- A new optional-Mode superclass called `AdvancedMode`;  AdvancedMode offers:
    - a "lifecycle type" (ball, game, system, or custom) --modes are auto added/removed based on that type. They only need to be created by importing them in the game code and creating them in init. Skeleton game adds/removed them as per their type 
    - a refined set of game progress events that get sent to AdvancedModes, in priority order, prior to the actual event occuring. Now modes themselves can respond directly to `evt_game_starting`, `evt_ball_starting`, `evt_ball_ending`, `evt_game_ending`, `evt_player_added`, `evt_tilt`, and `evt_tilt_ball_ending` events. Modes can also request to postpone the event propegation (i.e., the calling of the next event handler) by returning a number of seconds that the mode needs to 'finish up' (e.g., play a special animation or sound) or can delay and stop further propegation by returning a tuple of the delay in seconds and the second entry is `True`
- A small and hopefully well commented example game based on T2.

### Coming Soon: ###

- automatic handling of AC Relay coils (from yaml markup, only)
- ball search
- match mode
- more features to the bonus mode: using a yaml file to define about valid bonuses, score per award, Max numbers to allow of said award, etc. the tally is still in progress --this is not totally done.

# Getting Started #

0. get the pre-requisite libraries installed:

    - pyOSC
    - PySDL2 + SDL2.dll, SDL2_TTF.dll
    - OpenCV
    - (more added as I remember it)

1. Create your project workspace (folder structure):

    Assuming I put my game in a folder called ``MyGame`` my directory structure should look like:

        MyGame/
        |
        +--config/      [this is where most yaml files live]
        |
        +--assets/      [your asset_list.yaml is here as well as individual dmds, sounds, lampshows]
        |
        +--my_modes/    [.py files for the modes that you add to your game]
        |
        +--MyGame.py    [your game class]
        |
        +--config.yaml  [these are the settings for your game: dmd size, resolution, etc.]

    Before we can really begin, you need a ``config.yaml`` file and a machine yaml file.

2. ``config.yaml``

    Use the default provided.  TODO: Paste documetnation from pinballcontrollers forum

3. ``machine.yaml``

    This is the machine definition file.  It defines all the switches, lamps and coils in your machine.  Some samples are available.

    If using your own you must adhere to a few things:
        
      - your trough switches should be named ``trough1``, ``trough2``, .. ``troughN`` where N==num trough switches.
      - your start button should be called ``startButton``
      - your shooter lane switch should be called ``shooter``
      - your (bob) tilt switch should be called ``tilt``
      - your slam-tilt switch should be called ``slamTilt`` 

4. Build your ``asset_list.yaml``

    TODO: quite a lot to write about the format.  The example is probably good to reporoduce here.  

    You must be sure you define a few things:

      - A Font or HDFont named: `tilt-font-big`, `tilt-font-small`, `settings-font-small`, `high_score_entry_inits`, `high_score_entry_msg` `high_score_entry_letters`
      - blah blah
      - something else that's vital...

5. Other important yaml files:

    ###score_display.yaml###

```yaml
    ScoreLayout:
      Fonts:
            bottom_info:                  # the bottom info Credits/Ball Num
                  Font: score_sub         # value corresponds to a font key in asset_list.yaml
                  FontStyle: blueish      # FontStyles are also in asset_list and OPTIONAL
            single_player:                # Fonts/Styles for single player play
                  10_digits:
                        Font: score_activeL # corresponds to keys in asset_list.yaml
                  11_digits:
                        Font: score_activeM
                  12plus:
                        Font: score_activeS
            multiplayer:                 # Fonts/Styles for multiplayer play
                  active:                 # style for the active player
                        7_digits: 
                              Font: score_activeL
                        8_digits: 
                              Font: score_activeM
                        9plus: 
                              Font: score_activeS
                  inactive:               # style for the inactive player(s)
                        7_digits: 
                              Font: score_inactive
                        8_digits: 
                              Font: score_inactive
                        9plus: 
                              Font: score_inactive

```

###attract.yaml###
```yaml
        Sequence:
        - Combo:
            Text:
                - "MOcean"
                - ""
                - "Presents"
            Font: large
            lampshow: attract_show_1
            duration: 2.0
        - Animation:
            Name: t800-war
        - Combo:
            Text:
                - "Terminator"
                - ""
                - "2.0"
            Font: large
            Animation: chrome
            FontStyle: blueish
            lampshow: attract_show_2
            duration: 2.0
        - HighScores:
            Font: large
            Background: chrome
            Order:
                - player
                - category
                - score
            duration: 1.0
```

# GAME EVENT FLOW #

A game class that is subclassed from SkeletonGame should be very short.  The example provided is fewer than 60 lines if you exclude imports, comments and whitespace.  Most of your code should be present in your mode classes, instead.

Your game class should not call game_start, ball_end, etc.  It should also not need to subclass these methods.  You can, of course, do so, but you should not HAVE to.  SkeletonGame (and its constiutent parts, including the attract and bonus modes) will handle the successive event progression.  In a typical game, this looks like:

### Your game class iniitalizes itself in main(). ###
 Behind the scenes, super(SkeletonGame,self).__init__ does the following:

- initializes the sound controller
- finds the DMD settings from the config.yaml and sets up your display
- creates a lampshow controller
- loads all your assets from the asset_list.yaml file (shows the player a graphical loading bar)
- initializes and connects the ball_save and trough modes
- loads the OSC mode, bonus mode, score display 

Then, any AdvancedMode derived modes that you initialize are automatically added to skeletonGame's 'known modes' so it can add/remove them for you, based on their mode_type (game, ball, system, custom).  

### When you call reset(): ###

/about reset():/ The SkeletonGame version of reset() protects the modes that need to be in the game.  The old reset method would remove ALL modes from the game, but reset() in skeletonGame's will re-add modes that should not be removed and protect certain modes (e.g., the OSC controller) from being removed at all.

The last thing your reset() method should do is call: self.start_attract_mode()

Then, SkeletonGame takes over again, initiating the attract mode from the yaml file.
When the player presses the switch with the name 'startButton', SkeletonGame will automatically:

- find modes with method *evt_game_starting* and call them 
- find modes with method *evt_player_added* and call them
- find modes with method *evt_ball_starting* and call them 
- add a ball to the shooter lane.

Your modes hopefully do something here :)

When the ball drains and the trough is full, SkeletonGame will automatically:

- finds modes with method *evt_ball_ending* and calls them
- show the 'end of ball' and bonus sequence (if bonuses were awarded)
- if the balls number is *less than* the quantity specified in the machine yaml
    * find modes with method *evt_ball_starting* and call them (repeating the cycle)
- if the ball number is *greater than* the quantity specified in the machine yaml
    * finds modes with method *evt_game_ending* and calls them
    * checks the players score against the high scores.  If greater, the player may enter his/her scores
    * attract mode is shown again

So, the available events are:

```python
evt_player_added(player)
evt_game_starting
evt_ball_starting
evt_ball_ending(shoot_again, last_ball)
evt_game_ending

```

Using the framework:

1. From you atract mode (if you don't like the one included)

