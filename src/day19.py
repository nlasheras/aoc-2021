"""" https://adventofcode.com/2021/day/19 """

from itertools import product
from functools import cache
import re
from utils import Point

class Scanner:
    """A scanner with a index and a list of points of beacons"""
    def __init__(self, index):
        self.index = index
        self.beacons = []

    def __repr__(self) -> str:
        return f"scanner {self.index} with {len(self.beacons)} beacons"

    def __eq__(self, __o: 'Scanner') -> bool:
        return self.index == __o.index

def parse_input(filename):
    scanner_re = re.compile(r"--- scanner (\d+) ---")
    beacon_re = re.compile(r"(-?\d+),(-?\d+),(-?\d+)")
    with open(filename, "r", encoding="utf-8") as file:
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

orientations = range(24)
@cache
def rotation(i, point:Point):
    # To find all possible rotations we will rotate first in around x or y
    # axis and there we have 4 rotations around z axis
    z_amount = i % 4
    y_amount = x_amount = 0
    if i >= 16:
        y_amount = ((i - 16) // 4) + 1
        if y_amount == 2:
            # rotating twice around y is equivalent to twice around x
            y_amount = 3
    else:
        x_amount = i // 4

    def __rotate_x__(_v: Point):
        return Point(_v.x, _v.z, -_v.y)
    def __rotate_y__(_v: Point):
        return Point(_v.z, _v.y, -_v.x)
    def __rotate_z__(_v: Point):
        return Point(_v.y, -_v.x, _v.z)

    for _ in range(x_amount):
        point = __rotate_x__(point)
    for _ in range(y_amount):
        point = __rotate_y__(point)
    for _ in range(z_amount):
        point = __rotate_z__(point)
    return point

def find_overlaps(scanner1, scanner2):
    """Find a list of beacons of scanner1 that are present also on scanner2.
    Returns a list of tuples (point_in_1, point_in_2, distance reference beacon)"""

    # we calculate a matrix of distance from each beacon on the scanner to the rest of
    # the beacons in the same scanner
    mag1 = [[(pj - pi).length_squared() for pj in scanner1.beacons] for pi in scanner1.beacons]
    mag2 = [[(pj - pi).length_squared() for pj in scanner2.beacons] for pi in scanner2.beacons]

    # we find which one is the best beacon to use as reference point and return the
    # overlaps using that beacon as a reference point
    max_overlaps = []
    for _, point1 in enumerate(mag1):
        for _, point2 in enumerate(mag2):
            overlaps = []
            for k, mag_k in enumerate(point2):
                if mag_k in point1:
                    k_in_i = point1.index(mag_k)
                    point_in_2 = scanner2.beacons[k]
                    point_in_1 = scanner1.beacons[k_in_i]
                    overlap = (Point(point_in_1.x, point_in_1.y, point_in_1.z),
                               Point(point_in_2.x, point_in_2.y, point_in_2.z),
                               mag_k)
                    overlaps.append(overlap)
            if len(overlaps) > len(max_overlaps):
                max_overlaps = overlaps

    return max_overlaps

def find_transform(overlap_list):
    """From the list of overlap pairs I want to find a mapping function that
    transforms from scanner2 coordinate system into scanner1
        f(x2,y2,z2) = x1,y1,z1"""

    assert len(overlap_list) >= 12

    # procedure consists on trying all combinations of orientations for both scanners
    for rot1, rot2 in product(orientations, repeat=2):
        for reference_point in overlap_list:

            offset =  rotation(rot1, reference_point[0]) - rotation(rot2, reference_point[1])
            func = (lambda x, offset=offset, r=rot2: rotation(r, x) + offset)

            def test(overlap, _f = func):
                return (_f(overlap[1]) - overlap[0]).length_squared() == 0

            if all(map(test, overlap_list)):
                return func

    # with 12 overlaps we should be able to find a valid func
    assert False
    return None

def map_beacons(scanners):
    """Return a matrix of functions to map between beacon coordinate
    systems """

    # find the map of functions to translate from scanner coordinate systems
    mapping = {}
    for i, scanner1 in enumerate(scanners):
        mapping[i] = {}
        for j, scanner2 in enumerate(scanners):
            if i == j:
                continue # no need for mapping to the same scanner
            overlaps = find_overlaps(scanner1, scanner2)
            if len(overlaps) < 12:
                continue # from problem definition

            overlaps = list(sorted(overlaps, key=lambda p: p[2]))
            if func := find_transform(overlaps):
                mapping[i][j] = func

    # fill the missing transform function composing known ones
    count = len(scanners)
    for _ in range(count-1): # we may need more than 1 pass
        for i, j in product(range(count), repeat=2):
            # for all missing mapping functions try to find a posible composing
            if i != j and not j in mapping[i]:
                for k in range(count):
                    if i == k:
                        continue
                    if j in mapping[k] and k in mapping[i]:
                        # pylint: disable=line-too-long
                        composed = lambda x, _ii=i, _jj=j, _kk=k: mapping[_ii][_kk](mapping[_kk][_jj](x))
                        mapping[i][j] = composed

    return mapping

def main(filename):
    scanners = parse_input(filename)
    mapping = map_beacons(scanners)

    # Part 1: find unique positions from the coord system of one scanner
    pos_relative_to_0 = set()
    for _s in scanners:
        for _b in _s.beacons:
            _p = mapping[0][_s.index](_b) if _s.index != 0 else _b
            pos_relative_to_0.add((_p.x,_p.y,_p.z))
    print(f"How many beacons are there? {len(pos_relative_to_0)}")

    # Part 2: find the offset to all scanners assuming the scanner 0 coordinate
    # system as world origin
    scanner_pos = []
    scanner_pos.append(Point(0,0,0))
    count = len(scanners)
    for i in range(1,count):
        scanner_pos.append(mapping[0][i](Point(0,0,0)))

    def manhattan_distance(_p1, _p2):
        return abs(_p2.x - _p1.x) + abs(_p2.y - _p1.y) + abs(_p2.z - _p1.z)

    max_distance = 0
    for i, j in product(range(count), repeat=2):
        if i == j:
            continue
        max_distance = max(max_distance, manhattan_distance(scanner_pos[i], scanner_pos[j]))
    print(f"Max manhattan distance = {max_distance}")

if __name__ == '__main__':
    main("input19_test.txt")
    main("input19.txt")
