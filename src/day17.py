""" https://adventofcode.com/2021/day/17 """

import re
import math
from typing import Tuple

class Rect:
    """A 2D rectangle defined by top-left and bottom-right positions"""
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def inside(self, x, y):
        """Checks if a given x, y point is inside the rect"""
        return (self.left <= x <= self.right) and (self.bottom <= y <= self.top)

    @staticmethod
    def from_input(string):
        match = re.search(r"target area: x=(-?\d*)..(-?\d*), y=(-?\d*)..(-?\d*)", string)
        if match:
            left = int(match.group(1))
            right = int(match.group(2))
            bottom = int(match.group(3))
            top = int(match.group(4))
            return Rect(left, right, bottom, top)
        assert False # Shouldn't reach
        return None

def sign(_n):
    if _n > 0:
        return 1
    if _n < 0:
        return -1
    return 0

def hit_target(vx0, vy0, target:Rect) -> Tuple[bool, int]:
    """Simulate the probe shooting and check if the probe reaches the target area.
    Returns wether probe reaches the target area in a discrete t and, in that case,
    the maximum height it reaches on the trajectory."""
    velocity_x = vx0
    velocity_y = vy0
    probe_x = 0
    probe_y = 0
    _t = 0
    max_height = 0
    while probe_x < target.right and probe_y > target.bottom:
        probe_x += velocity_x
        probe_y += velocity_y
        max_height = max(max_height, probe_y)
        velocity_x -= sign(velocity_x)
        velocity_y -= 1
        _t += 1
        if target.inside(probe_x, probe_y):
            return True, max_height
    return False, 0

puzzle = Rect.from_input("target area: x=209..238, y=-86..-59")
example = Rect.from_input("target area: x=20..30, y=-10..-5")

def both_parts_bruteforce(target):
    global_maxima = 0
    hit_count = 0

    # do a smart brute-force over sensible ranges
    min_vx = 0
    max_vx = target.right # max speed is hitting the right of the area in t=1

    min_vy = min(target.bottom, target.top) # use the same reasoning as for maxvy
    max_vy = -min_vy # not much thinkin here (explore the same range in positive than in negative)

    for velocity_x in range(min_vx, max_vx+1):
        min_vx = math.floor((1 + math.sqrt(1 + target.left * 8)) / 2)
        max_vx = target.right
        for velocity_y in range(min_vy, max_vy+1):
            hit, maxy = hit_target(velocity_x, velocity_y, target)
            if hit:
                global_maxima = max(global_maxima, maxy)
                hit_count += 1

    print(f"What is the highest y position it reaches on this trajectory? {global_maxima}")
    print(f"How many distinct initial velocity values cause the probe to be within the target area after any step?: {hit_count}")

both_parts_bruteforce(example)
both_parts_bruteforce(puzzle)
