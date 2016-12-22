import os

from itertools import combinations

DIRS = UP, DOWN = 1, -1

from .facility import Facility

def load():
    return open(os.path.join(os.path.dirname(__file__), 'input.txt')).read()

def indent(fac, n=1):
    indent = '  ' * n
    lines = str(fac).splitlines()
    lines = (indent + line for line in lines)
    return '\n'.join(lines)

def test1():
    # Doesn't solve yet but does check that the Facility class reports and
    # moves it's state correctly.

    text = ("The first floor contains a hydrogen-compatible microchip and a"
            " lithium-compatible microchip.\n"
            "The second floor contains a hydrogen generator.\n"
            "The third floor contains a lithium generator.\n"
            "The fourth floor contains nothing relevant.\n")

    facility = Facility(text)
    assert facility.directions() == (UP, )

    line = '-' * 17

    moves = [(UP,   ('HM', )),
             (UP,   ('HG', 'HM')),
             (DOWN, ('HM', )),
             (DOWN, ('HM', )),
             (UP,   ('HM', 'LM')),
             (UP,   ('HM', 'LM')),
             (UP,   ('HM', 'LM')),
             (DOWN, ('HM', )),
             (UP,   ('HG', 'LG')),
             (DOWN, ('LM', )),
             (UP,   ('HM', 'LM'))]
    for move in moves:
        print(line)
        print(facility)
        assert not facility.solved()
        facility = facility.move(*move)
        assert facility.safe()

    assert facility.directions() == (DOWN, )
    assert facility.solved()
    print(line)
    print(facility)

def part1():
    facility = Facility(load())

# 1. elevator capacity two microchips or generators
# 2. elevator must have at least one microchip or generator to move
# 3. chip must be connected to its generator to exist on the same floor as a
# different generator

def main():
    test1()
    part1()
