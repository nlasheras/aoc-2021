""" https://adventofcode.com/2021/day/22 """

from __future__ import annotations
from typing import List
import re

class Range:
    """Represents a range of cubes from [min, max)"""
    def __init__(self, _min = (0,0,0), _max = (0,0,0)):
        self.min = _min
        self.max = _max

    def __repr__(self) -> str:
        return f"x={self.min[0]}..{self.max[0]} y={self.min[1]}..{self.max[1]} z={self.min[2]}..{self.max[2]}"

    def intersected(self, _range: Range):
        """Returns the Range of an intersection between self and range. When
        there is no intersection returns None"""
        imin = (max(self.min[0], _range.min[0]),
                max(self.min[1], _range.min[1]),
                max(self.min[2], _range.min[2]))
        imax = (min(self.max[0], _range.max[0]),
                min(self.max[1], _range.max[1]),
                min(self.max[2], _range.max[2]))
        if imin[0] >= imax[0] or imin[1] >= imax[1] or imin[2] >= imax[2]:
            return None
        return Range(imin, imax)

    def volume(self) -> int:
        return (self.max[0] - self.min[0]) * (self.max[1] - self.min[1]) * (self.max[2] - self.min[2])

    # Not used anymore (this was used in the original part1 simulating the procedure)
    def inside(self, pos) -> bool:
        """Check wether point p = (x,y,z) is inside the range"""
        return self.min[0] <= pos[0] < self.max[0] and \
               self.min[1] <= pos[1] < self.max[1] and \
               self.min[2] <= pos[2] < self.max[2]

class Cuboid:
    """A cuboid is an area of cubes in the grid that supports substraction"""
    def __init__(self, _range: Range):
        self.range = _range
        self.substracted: List[Cuboid] = []

    def substract(self, cuboid: Cuboid):
        """Substract the parameter cuboid from this"""
        sub_range = self.range.intersected(cuboid.range)
        if sub_range:
            # when no intersection between self and cuboid, nothing happens
            sub_cube = Cuboid(sub_range)
            # remove the new substraction from the rest of subtracted cuboids
            for _c in self.substracted:
                _c.substract(sub_cube)
            self.substracted += [sub_cube]

    def volume(self) -> int:
        vol = self.range.volume()
        for cuboid in self.substracted:
            vol -= cuboid.volume()
        return vol

class Step:
    """Each of the operations to be performed in the grid. Type is either
    "on" or "off" and then there is the range of cubes that operation affects"""
    def __init__(self, _type: str, _range: Range):
        self.type = _type
        self.range = _range

    def __repr__(self) -> str:
        return f"{self.type} {self.range}"

def parse_input(filename) -> List[Step]:
    with open(filename, "r", encoding="utf-8") as file:
        step_re = re.compile(r"(\w*) x=(-?\d*)..(-?\d*),y=(-?\d*)..(-?\d*),z=(-?\d*)..(-?\d*)")
        steps = []
        for line in file.readlines():
            if match := step_re.match(line):
                operation = match.group(1)
                step_min = (int(match.group(2)), int(match.group(4)), int(match.group(6)))
                # add 1 to the max to make the ranges [min, max)
                step_max = (int(match.group(3))+1, int(match.group(5))+1, int(match.group(7))+1)
                steps.append(Step(operation, Range(step_min, step_max)))
        return steps

def count_cubes(steps, bounds:Range = None):
    """In order to count the cubes the process consists on keeping a list of
    the "on" cuboids. In every step we add a Cuboid of the full Range for
    the step and we remove the cubes from that cuboid from all the previous
    cuboids"""
    cuboids: List[Cuboid] = []
    for _, s_i in enumerate(steps):
        range_i = s_i.range.intersected(bounds) if bounds else s_i.range
        if range_i is None:
            continue
        cuboid_i = Cuboid(range_i)
        for _c in cuboids:
            _c.substract(cuboid_i)
        if s_i.type == "on": # when cuboid is "off" it just removes the cubes
            cuboids.append(cuboid_i)
    return sum([c.volume() for c in cuboids])

def part1(filename):
    steps = parse_input(filename)
    count = count_cubes(steps, Range((-50,-50, -50), (51, 51, 51)))
    print(f"how many cubes are on between the initialization region? {count}")

def part2(filename):
    steps = parse_input(filename)
    count = count_cubes(steps)
    print(f"how many cubes are on? {count}")

if __name__ == '__main__':
    part1("input22_test1.txt")
    part1("input22_test2.txt")
    part1("input22.txt")
    part2("input22_test3.txt")
    part2("input22.txt")
