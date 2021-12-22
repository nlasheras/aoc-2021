# https://adventofcode.com/2021/day/22

from __future__ import annotations
from typing import List

class Range:
    """Represents a range of cubes from [min, max)"""
    def __init__(self, min = (0,0,0), max = (0,0,0)):
        self.min = min
        self.max = max
    
    def __repr__(self) -> str:
        return f"x={self.min[0]}..{self.max[0]} y={self.min[1]}..{self.max[1]} z={self.min[2]}..{self.max[2]}"
    
    def intersected(self, range: Range):
        """Returns the Range of an intersection between self and range. Whne there is no intersection returns None"""
        imin = (max(self.min[0], range.min[0]), max(self.min[1], range.min[1]), max(self.min[2], range.min[2]))
        imax = (min(self.max[0], range.max[0]), min(self.max[1], range.max[1]), min(self.max[2], range.max[2]))
        if imin[0] >= imax[0] or imin[1] >= imax[1] or imin[2] >= imax[2]:
            return None
        return Range(imin, imax)

    def volume(self) -> int:
        return (self.max[0] - self.min[0]) * (self.max[1] - self.min[1]) * (self.max[2] - self.min[2])

    # Not used anymore (this was used in the original part1 simulating the procedure)
    def inside(self, p) -> bool:
        """Check wether point p = (x,y,z) is inside the range"""
        return self.min[0] <= p[0] < self.max[0] and \
               self.min[1] <= p[1] < self.max[1] and \
               self.min[2] <= p[2] < self.max[2]

class Cuboid:
    """A cuboid is an area of cubes in the grid that supports substraction"""
    def __init__(self, range: Range):
        self.range = range
        self.substracted: List[Cuboid] = []
    
    def substract(self, cuboid: Cuboid):
        """Substract the parameter cuboid from this"""
        sub_range = self.range.intersected(cuboid.range)
        if sub_range:
            # when no intersection between self and cuboid, nothing happens
            sub_cube = Cuboid(sub_range)
            # remove the new substraction from the rest of subtracted cuboids
            for c in self.substracted:
                c.substract(sub_cube) 
            self.substracted += [sub_cube]

    def volume(self) -> int:
        v = self.range.volume()
        for c in self.substracted:
            v -= c.volume()
        return v
    
class Step:
    def __init__(self, type: str, range: Range):
        self.type = type
        self.range = range

    def __repr__(self) -> str:
        return f"{self.type} {self.range}"

import re

def parse_input(filename):
    with open(filename, "r") as file:
        step_re = re.compile("(\w*) x=(-?\d*)..(-?\d*),y=(-?\d*)..(-?\d*),z=(-?\d*)..(-?\d*)")
        steps = []
        for line in file.readlines():
            if m := step_re.match(line):
                type = m.group(1)
                min = (int(m.group(2)), int(m.group(4)), int(m.group(6)))
                # add 1 to the max to make the ranges [min, max)
                max = (int(m.group(3))+1, int(m.group(5))+1, int(m.group(7))+1)
                steps.append(Step(type, Range(min, max)))
        return steps

def count_cubes(steps, bounds:Range = None):
    # in order to count the cubes the process consists on keeping a list of 
    # the "on" cuboids. In every step we add a Cuboid of the full Range for 
    # the step and we remove the cubes from that cuboid from all the previous
    # cuboids
    cuboids: List[Cuboid] = []
    for i, s_i in enumerate(steps):
        range_i = s_i.range.intersected(bounds) if bounds else s_i.range
        if range_i is None:
            continue
        cuboid_i = Cuboid(range_i)
        for c in cuboids:
            c.substract(cuboid_i)
        if s_i.type == "on": # when cuboid is "off" it just removes the cubes
            cuboids.append(cuboid_i) 
    return sum([c.volume() for c in cuboids])

def part1(filename):
    steps = parse_input(filename)
    c = count_cubes(steps, Range((-50,-50, -50), (51, 51, 51)))
    print(f"how many cubes are on between the initialization region? {c}")

def part2(filename):
    steps = parse_input(filename)
    c = count_cubes(steps)
    print(f"how many cubes are on? {c}")

if __name__ == '__main__':
    part1("input22_test1.txt")
    part1("input22_test2.txt")
    part1("input22.txt")
    part2("input22_test3.txt")
    part2("input22.txt")