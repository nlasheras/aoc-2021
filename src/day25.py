# https://adventofcode.com/2021/day/25

from utils import Grid

def step(cucumbers: set, cols, rows):
    count = 0
    new_cucumbers = set()
    # horizontal pass
    for c in cucumbers: 
        if c[0] == '>':
            pos = (c[1] + 1, c[2]) if c[1] < cols-1 else (0, c[2])
            if ('>', pos[0], pos[1]) not in cucumbers and \
               ('v', pos[0], pos[1]) not in cucumbers:
                    new_cucumbers.add(('>', pos[0], pos[1]))
                    count += 1
            else:
                new_cucumbers.add(c)
    # vertical pass
    for c in cucumbers: 
        if c[0] == 'v':
            pos = (c[1], c[2]+1) if c[2] < rows-1 else (c[1], 0)
            if ('>', pos[0], pos[1]) not in new_cucumbers and \
               ('v', pos[0], pos[1]) not in cucumbers:
                    new_cucumbers.add(('v', pos[0], pos[1]))
                    count += 1
            else:
                new_cucumbers.add(c)
    return new_cucumbers, count

def render(set, cols, rows):
    render = ""
    for row in range(rows):
        for col in range(cols):
            if ('>', col, row) in set:
                render += '>'
            elif ('v', col, row) in set:
                render += 'v'
            else:
                render += '.'
        render += "\n"
    return render

def parse_input(filename):
    g = Grid(filename, str)

    cucumbers = set()
    for row in range(g.rows):
        for col in range(g.cols):
            idx = g.get_idx((col, row))
            if g.cells[idx] != '.':
                cucumbers.add((g.cells[idx], col, row))
    
    return cucumbers, g.cols, g.rows

def part1(filename):
    cucumbers, cols, rows = parse_input(filename)

    steps = 0
    while True:
        cucumbers, moves = step(cucumbers, cols, rows)
        steps += 1
        if moves == 0:
            break
    
    return steps
    
import sys
if __name__ == '__main__':
    file = sys.argv[1] if len(sys.argv) > 1 else "input25.txt"
    steps = part1(file)
    print(f"What is the first step on which no sea cucumbers move? {steps}")