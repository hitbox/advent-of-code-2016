import os
import re

class Room(object):

    _room_re = re.compile('^(.*)-(\d+)\[([a-z]+)\]$')

    def __init__(self, name):
        self.name = name

    def parse_room(self):
        m = self._room_re.match(self.name)
        if m:
            encrypted, sectorid, checksum = m.groups()
            return (encrypted, int(sectorid), checksum)

    def mostcommon(self):
        rv = self.parse_room()
        if not rv:
            return
        encrypted_name, _, _ = rv
        s = ''.join(encrypted_name.split('-'))
        d = {}
        for c in s:
            if c not in d:
                d[c] = 0
            d[c] += 1
        charcounts = ((c, d[c]) for c in set(s) )
        return sorted(sorted(charcounts, key=lambda t: t[0]), key=lambda t: t[1], reverse=True)

    def encryptedchecksum(self):
        rv = ''.join(c for i,c in enumerate(char for char,count in self.mostcommon()) if i < 5)
        return rv

    def is_real(self):
        rv = self.parse_room()
        if rv:
            _, _, checksum = rv
            return self.encryptedchecksum() == checksum
        return False

    def sectorid(self):
        rv = self.parse_room()
        if rv:
            return rv[1]


def tests():
    sector_total = 0

    room = Room('aaaaa-bbb-z-y-x-123[abxyz]')
    assert room.is_real()
    sector_total += room.sectorid()

    room = Room('a-b-c-d-e-f-g-h-987[abcde]')
    assert room.is_real()
    sector_total += room.sectorid()

    room = Room('not-a-real-room-404[oarel]')
    assert room.is_real()
    sector_total += room.sectorid()

    room = Room('totally-real-room-200[decoy]')
    assert not room.is_real()

    assert sector_total == 1514

def load():
    return open(os.path.join(os.path.dirname(__file__), 'input.txt')).readlines()

def main():
    tests()

    total = 0
    for line in load():
        room = Room(line)
        if room.is_real():
            total += room.sectorid()

    print('Day 4, part 1: total sector id is %s' % total)
