"""gummworld2.py - startup and runtime settings file

This file is part of Gummworld2.

Gummworld2 is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Gummworld2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with Gummworld2.  If not, see <http://www.gnu.org/licenses/>.

Usage
=====
Settings in this file should always be accessed like so:
    
    import settings
    if settings.whatever: ...
    settings.whatever = value

This insures that runtime changes will be noticed by other modules that import
the settings module. Of course, one can always make local copies of the values
if static behavior is desired.
"""

__version__ = '1.0'

import pygame

import gummworld2


## Display
resolution = 800,600        # screen size in pixels: width,height
fullscreen = False          # open fullscreen if True
update_speed = 30           # physics ticks/sec; clock uses fixed time step
frame_speed = 0             # frame throttle frames/sec; 0=unlimited

## Game
# Map size is specified as number of tiles (X,Y):
#map_size = (312,312)        # small map (tile size = 16x16 pixels)
map_size = (1000,312)       # large map (tile size = 16x16 pixels)
player_speed = 3.0          # how fast player walks


## Graphics
# Defaults already set for graphics asset paths. You can add new subdirs like so.
#gummworld2.data.set_subdir('myname', 'subdir')

## Sound
# Defaults already set for sound asset paths. You can add new subdirs like so.
gummworld2.data.set_subdir('music', 'music')

## UI
fgcolor = pygame.Color(135, 206, 250)
bgcolor = pygame.Color(52, 69, 52)
bgcolor = pygame.Color(31, 41, 31)
KEYS = dict(
    left  = (pygame.K_LEFT,pygame.K_a),
    right = (pygame.K_RIGHT,pygame.K_d),
    jump  = (pygame.K_SPACE,pygame.K_UP,pygame.K_w),
    swaptool = (pygame.K_TAB,),
)

## Debug
profile = False                             # run cProfile if True
#bypass_menu = (None, 'game', 'credits')[0]  # bypass mainmenu
debug_lighting = False

## Custom
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Gummbum's development preferences... remove or add a case for your own.
who = 'Gumm'
try:
    if who == 'Gumm':
        print '## CUSTOM SETTINGS FOR Gumm (see settings.py)'
        bypass_menu = (None, 'game', 'credits')[1]
        map_size = (312,312)
        map_size = (128,128)
except:
    pass

del os,who
