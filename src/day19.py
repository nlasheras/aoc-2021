# https://adventofcode.com/2021/day/19

from itertools import permutations
from itertools import product
from utils import Point

class Scanner:
    def __init__(self, index):
        self.index = index
        self.beacons = []

    def __repr__(self) -> str:
        return f"scanner {self.index} with {len(self.beacons)} beacons"

import re 
def parse_input(filename):
    scanner_re = re.compile("--- scanner (\d+) ---")
    beacon_re = re.compile("(-?\d+),(-?\d+),(-?\d+)")
    with open(filename, "r") as file:
        scanners = []
        for line in file.readlines():
            if match := scanner_re.match(line):
                index = int(match.group(1))
                scanners.append(Scanner(index))
            elif match := beacon_re.match(line):
                x = int(match.group(1))
                y = int(match.group(2))
                z = int(match.group(3))
                scanners[-1].beacons.append(Point(x, y, z))
        return scanners

# This rotation also contain the mirrored space with 48 orientations
orientations = range(48)
digit_perm = list(permutations(range(3)))
sign_changes = list(product([1,-1], repeat=3))
def rotation(i, v:Point):
    perm = digit_perm[i // 8]
    sign = sign_changes[i % 8]

    def sign_component(i):
        return sign[i]

    def component(v: Point, i):
        if i == 0: return v.x
        elif i == 1: return v.y
        elif i == 2: return v.z

    x = component(v, perm[0]) * sign_component(perm[0])
    y = component(v, perm[1]) * sign_component(perm[1])
    z = component(v, perm[2]) * sign_component(perm[2])
    return Point(x, y, z)

def find_overlaps(s1, s2):
    t1 = Point(1,2,3)
    t2 = Point(4,0,-1)
    t = t2 - t1
    mag1 = [[(pj - pi).length_squared() for pj in s1.beacons] for pi in s1.beacons]
    mag2 = [[(pj - pi).length_squared() for pj in s2.beacons] for pi in s2.beacons]

    max_overlaps = []
    for i, v1 in enumerate(mag1):
        for j, v2 in enumerate(mag2):
            overlaps = []
            for k, mag_k in enumerate(v2):
                if mag_k in v1:
                    k_in_i = v1.index(mag_k)
                    p2 = s2.beacons[k]
                    p1 = s1.beacons[k_in_i]
                    t = (Point(p1.x,p1.y,p1.z), Point(p2.x, p2.y, p2.z), mag_k)
                    overlaps.append(t)
            if len(overlaps) > len(max_overlaps):
                max_overlaps = overlaps

    return max_overlaps

# from a list of overlap pairs I want to find a f(x2,y2,z2) = x1,y1,z1
def find_transform(overlap_list):
    for r1, r2 in product(orientations, repeat=2):
        for p0 in overlap_list:
            offset0 =  rotation(r1, p0[0]) - rotation(r2, p0[1])
            valid = True
            f = (lambda x, offset=offset0, r=r2: rotation(r, x) + offset)
            for p in overlap_list:
                test = f(p[1])
                if (test - p[0]).length_squared() > 0:
                    valid = False
                    break
            if valid:
                return f
    return None

def map_beacons(filename):
    scanners = parse_input(filename)

    # find the map of functions to translate from scanner coordinate systems
    fs = {}
    for i, s1 in enumerate(scanners):
        fs[i] = {}
        for j, s2 in enumerate(scanners):
            if j == i: 
                continue
            overlaps = find_overlaps(s1, s2)
            if (len(overlaps) < 12):
                continue 
            
            overlaps = list(sorted(overlaps, key=lambda p: p[2]))
            if f := find_transform(overlaps):
                fs[i][j] = f

    # fill the missing transform function composing known ones
    count = len(scanners)
    for p in range(count): # need more than 1 pass
        for i in range(count):
            for j in range(count):
                if i == j: continue
                if not j in fs[i]:
                    for k in range(count):
                        if i == k: continue
                        if j in fs[k] and k in fs[i]:
                            fs[i][j] = lambda x, ii=i, jj=j, kk=k: fs[ii][kk](fs[kk][jj](x))

    # Part 1: find unique positions from the coord system of one scanner
    pos_relative_to_0 = set()
    for i,s in enumerate(scanners):
        for b in s.beacons:
            p = fs[0][s.index](b) if s.index != 0 else b
            pos_relative_to_0.add((p.x,p.y,p.z))
    print(f"How many beacons are there? {len(pos_relative_to_0)}")
    
    # Part 2: find the offset to all scanners assuming the scanner 0 coordinate 
    # system as world origin
    scanner_pos = []
    scanner_pos.append(Point(0,0,0))
    for i in range(1,count):
        scanner_pos.append(fs[0][i](Point(0,0,0)))

    def manhattan_distance(p1, p2):
        return abs(p2.x - p1.x) + abs(p2.y - p1.y) + abs(p2.z - p1.z)

    max_distance = 0
    for i in range(count):
        for j in range(count):
            if i == j: continue
            max_distance = max(max_distance, manhattan_distance(scanner_pos[i], scanner_pos[j]))
    print(f"Max manhattan distance = {max_distance}")

if __name__ == '__main__':
    map_beacons("input19_test.txt")
    map_beacons("input19.txt")