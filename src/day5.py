""" https://adventofcode.com/2021/day/5 """

import sys
import re
from functools import reduce
from utils import Point
from utils import Grid

def normalized(self):
    """Not really a proper normalization, but just getting the sign of each component"""
    def __sign__(x):
        if x == 0:
            return 0
        return 1 if x > 0 else -1

    return Point(__sign__(self.x), __sign__(self.y))


def read_input(input_file):
    with open(input_file, newline='',encoding='utf-8') as file:
        input_lines = file.readlines()
        input_re = re.compile(r"(\d*),(\d*) -> (\d*),(\d*)")

        lines = []
        for line in input_lines:
            match = input_re.match(line)
            start_point = Point(int(match.group(1)), int(match.group(2)))
            end_point = Point(int(match.group(3)), int(match.group(4)))
            lines += [(start_point, end_point)]

        return lines

def render_lines(grid, lines, include_diagonal = False):
    for line in lines:
        start = line[0]
        end = line[1]
        line_direction = normalized(end - start)

        if not include_diagonal and line_direction.x != 0 and line_direction.y != 0:
            continue

        current = Point(start.x, start.y)
        while True:
            idx = current.y*grid.cols + current.x
            grid.cells[idx] += 1
            if current == end:
                break
            current += line_direction

def count_overlaps(lines, grid_width, grid_height, include_diagonals = False):
    grid = Grid.empty(grid_width, grid_height, 0)
    render_lines(grid, lines, include_diagonals)
    if grid_width <= 10 and grid_height <= 10:
        print(grid.render())
    return reduce(lambda acc, x: acc + 1, [x for x in grid.cells if x >= 2], 0)

def main(input_file):
    lines = read_input(input_file)

    max_x = reduce(max, [max(l[0].x, l[1].x) for l in lines])
    max_y = reduce(max, [max(l[0].y, l[1].y) for l in lines])

    overlap_count = count_overlaps(lines, max_x+1, max_y+1)
    print(f"At how many points do at least two lines overlap? {overlap_count}")

    overlap_count = count_overlaps(lines, max_x+1, max_y+1, True)
    print(f"At how many points do at least two lines overlap (including diagonal)? {overlap_count}")

    print("\n")

if __name__ == '__main__':
    INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input5.txt"
    main("input5_test.txt")
    main(INPUT_FILE)
