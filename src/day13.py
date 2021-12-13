# https://adventofcode.com/2021/day/13

from functools import reduce

class Paper:
    def __init__(self):
        self.dots = set()
    
    def __fold__(self, func):
        self.dots = set(map(func, self.dots))

    def fold_left(self, x):
        def get_folded_pos(p):
            return (2*x - p[0] if p[0] >= x else p[0], p[1])
        self.__fold__(get_folded_pos)

    def fold_up(self, y):
        def get_folded_pos(p):
            return (p[0], 2*y - p[1] if p[1] >= y else p[1])
        self.__fold__(get_folded_pos)

    def print(self):
        max = reduce(lambda acc, p: (p[0] if p[0]>acc[0] else acc[0], p[1] if p[1] > acc[1] else acc[1]), self.dots)
        render = ""
        for y in range(max[1]+1):
            for x in range(max[0]+1):
                if (x, y) in self.dots:
                    render += "#"
                else:
                    render += "."
            render += "\n"
        print(render, end='')

import re
def read_input(filename):
    with open(filename, "r") as file:
        p = Paper()
        commands = []
        lines = file.readlines()
        dot_re = re.compile("(\d+),(\d+)")
        fold_re = re.compile("fold along (\w)=(\d+)")

        reached_commands = False
        for l in lines:
            if not reached_commands and (match := dot_re.search(l)):
                p.dots.add((int(match.group(1)), int(match.group(2))))
            elif match := fold_re.search(l):
                commands.append((match.group(1), int(match.group(2))))
        return (p, commands)


def part1_count_dots(filename):
    p, commands = read_input(filename)
    for c in commands[:1]:
        if c[0] == "x":
            p.fold_left(c[1])
        elif c[0] == "y":
            p.fold_up(c[1])
    print(f"How many dots are visible after completing just the first fold instruction on your transparent paper? {len(p.dots)}")

def part2_print(filename):
    p, commands = read_input(filename)
    for c in commands:
        if c[0] == "x":
            p.fold_left(c[1])
        elif c[0] == "y":
            p.fold_up(c[1])
    p.print()

if __name__ == '__main__':
    part1_count_dots("input13_test.txt")
    part1_count_dots("input13.txt")

    part2_print("input13_test.txt")
    part2_print("input13.txt")