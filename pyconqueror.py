#!/usr/bin/env python

from __future__ import print_function

import os
import time
import shutil
from itertools import count
from importlib import import_module

from jinja2 import Template


NORTH, EAST, SOUTH, WEST = range(4)


class Ability(object):
    """Ability class"""
    def __init__(self, warrior):
        """initialise object"""
        self.warrior = warrior

    def walk(self, direction=None):
        """Move in the given direction (forward by default)."""
        if direction:
            self.warrior.direction = direction
        if self.warrior.direction == NORTH:
            self.warrior.position[1] -= 1
        elif self.warrior.direction == EAST:
            self.warrior.position[0] += 1
        elif self.warrior.direction == SOUTH:
            self.warrior.position[1] += 1
        elif self.warrior.direction == WEST:
            self.warrior.position[0] -= 1


class Warrior(object):
    """Warrior class"""
    name = 'Warrior'

    def __init__(self, position=None, direction=EAST):
        """"initialise warrior"""
        self.position = position if position else [0, 0]
        self.direction = direction
        self.ability = Ability(self)

    def abilities(self):
        """
        get the list of abilities
        """
        return [(a, getattr(self.ability, a).__doc__)
                for a in dir(self.ability) if not a.startswith('_')]

    def __getattr__(self, attr):
        return getattr(self.ability, attr)


class Floor(object):
    """
    """
    def __init__(self, size):
        self.size = size

    def draw(self, warrior, stairs):
        print('  ' + '-' * self.size[0])
        for y in range(self.size[1]):
            print(' |', end='')
            for x in range(self.size[0]):
                if [x, y] == warrior:
                    print('@', end='')
                elif (x, y) == stairs:
                    print('>', end='')
                else:
                    print(' ', end='')
            print('|')
        print('  ' + '-' * self.size[0])


def run(level):
    """
    """
    if not level:
        return
    floor = Floor(level.size)
    player = import_module('.player', 'profile').Player()
    print('Starting the game...')
    floor.draw(level.warrior.position, level.stairs)
    for turn in count(1):
        print('Turn {0}'.format(turn))
        player.play_turn(level.warrior)
        floor.draw(level.warrior.position, level.stairs)
        if tuple(level.warrior.position) == level.stairs:
            print('Hurray! you have made it')
            break
        time.sleep(1)


def main(level_number):
    """
    """
    level = import_module('.level_{0:03}'.format(level_number), 'levels')
    level.number = level_number

    if not os.path.exists('profile/player.py'):
        try:
            os.makedirs('profile')
        except:
            pass
        open('profile/__init__.py', 'w').close()
        with open('templates/README.jinja') as f:
            template = Template(f.read())
            readme = template.render(level=level)

        shutil.copy('templates/player.py', 'profile/player.py')
        with open('profile/README', 'w') as f:
            f.write(readme)

        print("""
Check the README file in the porfile folder. Update the player.py file and run
it again.
        """)
        return None
    return level

if __name__ == '__main__':
    run(main(1))
