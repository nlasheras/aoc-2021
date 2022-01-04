""" https://adventofcode.com/2021/day/25 """

import sys
from utils import Grid

def step(cucumbers: set, cols, rows):
    """Simulate 1 step of the sea cucumber set in a cols x rows grid"""
    count = 0
    new_cucumbers = set()
    # horizontal pass
    for _c in cucumbers:
        if _c[0] == '>':
            pos = (_c[1] + 1, _c[2]) if _c[1] < cols-1 else (0, _c[2])
            if ('>', pos[0], pos[1]) not in cucumbers and \
               ('v', pos[0], pos[1]) not in cucumbers:
                new_cucumbers.add(('>', pos[0], pos[1]))
                count += 1
            else:
                new_cucumbers.add(_c)
    # vertical pass
    for _c in cucumbers:
        if _c[0] == 'v':
            pos = (_c[1], _c[2]+1) if _c[2] < rows-1 else (_c[1], 0)
            if ('>', pos[0], pos[1]) not in new_cucumbers and \
               ('v', pos[0], pos[1]) not in cucumbers:
                new_cucumbers.add(('v', pos[0], pos[1]))
                count += 1
            else:
                new_cucumbers.add(_c)
    return new_cucumbers, count

def render(cucumber_set, cols, rows):
    result = ""
    for row in range(rows):
        for col in range(cols):
            if ('>', col, row) in cucumber_set:
                result += '>'
            elif ('v', col, row) in cucumber_set:
                result += 'v'
            else:
                result += '.'
        result += "\n"
    return result

def parse_input(filename):
    grid = Grid.from_file(filename, str)

    cucumbers = set()
    for pos in grid.positions():
        if grid.get_value(pos) != '.':
            cucumbers.add((grid.get_value(pos), pos[0], pos[1]))

    return cucumbers, grid.cols, grid.rows

def part1(filename):
    cucumbers, cols, rows = parse_input(filename)

    _step = 0
    while True:
        cucumbers, moves = step(cucumbers, cols, rows)
        _step += 1
        if moves == 0:
            break

    return _step

if __name__ == '__main__':
    INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input25.txt"
    steps = part1(INPUT_FILE)
    print(f"What is the first step on which no sea cucumbers move? {steps}")
