""" https://adventofcode.com/2021/day/2 """

import sys

def part1_run_commands(commands):
    x = 0
    depth = 0
    for (opcode, amount) in commands:
        if opcode == "forward":
            x += amount
        elif opcode == "down":
            depth += amount
        elif  opcode == "up":
            depth -= amount
    return (x, depth)

def part2_run_commands(commands):
    x = 0
    depth = 0
    aim = 0
    for (opcode, amount) in commands:
        if opcode == "forward":
            x += amount
            depth += aim * amount
        elif opcode == "down":
            aim += amount
        elif  opcode == "up":
            aim -= amount
    return (x, depth)

if __name__ == '__main__':
    INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input2.txt"
    with open(INPUT_FILE, newline='',encoding='utf-8') as file:

        def parse_command(line):
            strings = line.split(" ")
            return (strings[0], int(strings[1]))
        input_commands = [parse_command(l) for l in file.readlines()]

        (final_x, final_depth) = part1_run_commands(input_commands)

        print(f"What do you get if you multiply your final horizontal position \
by your final depth?: {final_x*final_depth}")

        (final_x, final_depth) = part2_run_commands(input_commands)

        print(f"What do you get if you multiply your final horizontal position \
by your final depth?: {final_x*final_depth}")
    