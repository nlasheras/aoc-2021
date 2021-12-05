# https://adventofcode.com/2021/day/5

import sys
import re
from functools import reduce

class Point: 
    x = 0
    y = 0

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def normalized(self):
        def _normalize(x):
            abs = x if x >= 0 else -x
            return int(x/abs) if x != 0 else 0

        return Point(_normalize(self.x), _normalize(self.y))
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def read_input(input_file):
    with open(input_file, newline='',encoding='utf-8') as file:
        lines = file.readlines()
        input_re = re.compile(r"(\d*),(\d*) -> (\d*),(\d*)")

        input = []
        for l in lines:
            match = input_re.match(l)
            p1 = Point(int(match.group(1)), int(match.group(2)))
            p2 = Point(int(match.group(3)), int(match.group(4)))
            input += [(p1, p2)]
        
        return input

def render_lines(grid, grid_width, grid_height, lines, include_diagonal = False):
    for l in lines:
        start = l[0]
        end = l[1]
        dir = (end - start).normalized()

        if not include_diagonal and dir.x != 0 and dir.y != 0:
            continue 

        current = start
        while (True): 
            idx = current.y*grid_width + current.x
            grid[idx] += 1
            current += dir
            if (current == end):
                break

def render_grid(grid, grid_width, grid_height):
    render = ""
    for y in range(grid_height):
        for x in range(grid_width):
            value = grid[y*grid_width + x]
            render += str(value) if value > 0 else "."
        render += "\n"
    print(render)

def count_overlaps(lines, grid_width, grid_height, include_diagonals = False):
    grid = [0] * grid_width * grid_height
    render_lines(grid, grid_width, grid_height, lines, include_diagonals)
    if grid_width <= 10 and grid_height <= 10:
        render_grid(grid, grid_width, grid_height)
    return reduce(lambda acc, x: acc + 1, [x for x in grid if x >= 2], 0)

def main(input_file):
    lines = read_input(input_file)

    max_x = reduce(lambda x, acc: max(x, acc), [max(l[0].x, l[1].x) for l in lines])
    max_y = reduce(lambda x, acc: max(x, acc), [max(l[0].y, l[1].y) for l in lines])

    overlap_count = count_overlaps(lines, max_x+1, max_y+1)
    print(f"At how many points do at least two lines overlap? {overlap_count}")

    overlap_count = count_overlaps(lines, max_x+1, max_y+1, True)
    print(f"At how many points do at least two lines overlap (including diagonal)? {overlap_count}")


input_file = sys.argv[1] if len(sys.argv) > 1 else "input5.txt"
main("input5_test.txt")
main(input_file)

