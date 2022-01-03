""" https://adventofcode.com/2021/day/13 """

from functools import reduce
import re

class Paper:
    """Implements the paper and supports the fold left and up operations"""
    def __init__(self):
        self.dots = set()

    def __fold__(self, func):
        self.dots = set(map(func, self.dots))

    def fold_left(self, x):
        """Fold the paper left along the given x position"""
        def get_folded_pos(pos):
            return (2*x - pos[0] if pos[0] >= x else pos[0], pos[1])
        self.__fold__(get_folded_pos)

    def fold_up(self, y):
        """Fold the paper up along the given y position"""
        def get_folded_pos(pos):
            return (pos[0], 2*y - pos[1] if pos[1] >= y else pos[1])
        self.__fold__(get_folded_pos)

    def render(self):
        max_x = reduce(max, [pos[0] for pos in self.dots])
        max_y = reduce(max, [pos[1] for pos in self.dots])
        render = ""
        for y in range(max_y+1):
            for x in range(max_x+1):
                if (x, y) in self.dots:
                    render += "#"
                else:
                    render += "."
            render += "\n"
        return render

def read_input(filename):
    """Return a tuple with the Paper and the commands from the input file"""
    with open(filename, "r", encoding="utf-8") as file:
        paper = Paper()
        commands = []
        dot_re = re.compile(r"(\d+),(\d+)")
        fold_re = re.compile(r"fold along (\w)=(\d+)")

        reached_commands = False
        for line in file.readlines():
            if not reached_commands and (match := dot_re.search(line)):
                paper.dots.add((int(match.group(1)), int(match.group(2))))
            elif match := fold_re.search(line):
                commands.append((match.group(1), int(match.group(2))))
        return (paper, commands)

def apply_command(paper: Paper, command):
    if command[0] == "x":
        paper.fold_left(command[1])
    elif command[0] == "y":
        paper.fold_up(command[1])

def part1_count_dots(filename):
    """Apply only first command and count the amount of dots"""
    paper, commands = read_input(filename)
    apply_command(paper, commands[0])
    print(f"How many dots are visible after completing just the first fold instruction on your transparent paper? {len(paper.dots)}")

def part2_print(filename):
    paper, commands = read_input(filename)
    for _c in commands:
        apply_command(paper, _c)
    print(paper.render())

if __name__ == '__main__':
    part1_count_dots("input13_test.txt")
    part1_count_dots("input13.txt")

    part2_print("input13_test.txt")
    part2_print("input13.txt")
