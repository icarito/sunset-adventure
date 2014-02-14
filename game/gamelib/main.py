"""main.py - sets up the main application environment and launches the intro

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
"""

import cProfile, pstats

import gummworld2

import settings, intro, terrain, credits


def start_context():
    gummworld2.run(terrain.TerrainLoader(*settings.map_size))
    quit()


def main():
    global start_context
    if settings.profile:
        cProfile.run('start_context()', 'prof.dat')
        p = pstats.Stats('prof.dat')
        p.sort_stats('time').print_stats()
    else:
        start_context()
