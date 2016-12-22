import copy
import re

from itertools import combinations, starmap

from . import UP, DOWN, DIRS

class Facility(object):

    def __init__(self, text=None):
        self.elevator = 0
        self.floors = []
        if text is not None:
            self.parse(text)

    def parse(self, text):
        generators = re.compile('(\w+ generator)').findall
        microchips = re.compile('(\w+-compatible microchip)').findall

        def items(line):
            return generators(line) + microchips(line)

        def abbrev(full):
            sep = ' ' if ' ' in full else '-'
            return ''.join(part[0].upper() for part in full.split(sep))

        self.floors = [set(map(abbrev, items(line))) for line in text.splitlines()]
        nfloors = len(self.floors)

        self.dirmap = {0: (UP, ), nfloors-1: (DOWN, )}
        for fn in range(1, nfloors-1):
            self.dirmap[fn] = DIRS

    def __eq__(self, other):
        return (self.elevator == other.elevator
                and all(set(a) == set(b) for a,b in
                        zip(self.floors, other.floors)))

    def __str__(self):
        nitems = len(self.items())
        fmt = 'F{} {:2} {}'.format

        def fmtline(fn, items):
            has_elevator = self.elevator == fn
            e = 'E' if has_elevator else ''
            padded = list(sorted(items)) + ['.' for _ in range(nitems - len(items))]
            return fmt(fn + 1, e, ' '.join('{:2}'.format(item) for item in padded))

        return '\n'.join(starmap(fmtline, sorted(enumerate(self.floors), reverse=True)))

    def copy(self):
        facility = Facility()
        facility.elevator = self.elevator
        facility.floors = copy.deepcopy(self.floors)
        facility.dirmap = self.dirmap
        return facility

    def current(self):
        """
        Items on the current floor.
        """
        return self.floors[self.elevator]

    def directions(self):
        """
        Possible directions the elevator can physically move.
        """
        return self.dirmap[self.elevator]

    def enumfloors(self):
        return enumerate(self.floors, start=1)

    def items(self):
        """
        All items across all floors.
        """
        return [item for floor in self.floors for item in floor]

    def move(self, direction, items):
        fac = self.copy()
        for item in items:
            fac.floors[fac.elevator].remove(item)
            fac.floors[fac.elevator + direction].add(item)
        fac.elevator += direction
        return fac

    def safe(self):
        """
        Is the current state valid/safe?
        """
        for items in self.floors:
            gens = ''.join(item[0] for item in items if item[1] == 'G')
            chips = ''.join(item[0] for item in items if item[1] == 'M')
            if chips and gens:
                if not all(chip in gens for chip in chips):
                    return False
        return True

    def solved(self):
        """
        Solved if all items on top floor.
        """
        return set(self.floors[-1]) == set(self.items())
