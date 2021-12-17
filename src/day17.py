# https://adventofcode.com/2021/day/17

import re
class Rect:
    def __init__(self, left, right, bottom, up):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.up = up
    
    def inside(self, x, y):
        if (self.left <= x <= self.right) and (self.bottom <= y <= self.up):
           return True
        return False

    def from_input(string):
        match = re.search("target area: x=(-?\d*)..(-?\d*), y=(-?\d*)..(-?\d*)", string)
        if match:
            return Rect(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))

def sign(n):
    if n > 0: return 1
    elif n < 0: return -1
    return 0

def hit_target(vx0, vy0, target):
    vx = vx0
    vy = vy0
    px = 0
    py = 0
    t = 0
    max_height = 0
    while px < target.right and py > target.bottom: 
        px += vx
        py += vy
        max_height = max(max_height, py)
        vx -= sign(vx)
        vy -= 1
        t += 1
        if target.inside(px, py):
            return True, max_height
    return False, 0

puzzle = Rect.from_input("target area: x=209..238, y=-86..-59")
example = Rect.from_input("target area: x=20..30, y=-10..-5")

import math
def both_parts_bruteforce(target):
    global_maxima = 0
    hit_count = 0
    
    # do a smart brute-force over sensible ranges
    minvx = 0
    maxvx = target.right # max speed is hitting the right of the area in t=1

    minvy = min(target.bottom, target.up) # use the same reasoning as for maxvy
    maxvy = -minvy # not much thinkin here (explore the same range in the positive than the negatives)

    for vx in range(minvx, maxvx+1):
        minvx = math.floor((1 + math.sqrt(1 + target.left * 8)) / 2)
        maxvx = target.right
        for vy in range(minvy, maxvy+1):
            hit, maxy = hit_target(vx, vy, target)
            if hit:
                global_maxima = max(global_maxima, maxy)
                hit_count += 1

    print(f"What is the highest y position it reaches on this trajectory? {global_maxima}")
    print(f"How many distinct initial velocity values cause the probe to be within the target area after any step?: {hit_count}")

both_parts_bruteforce(example)
both_parts_bruteforce(puzzle)
