#https://adventofcode.com/2021/day/2

import sys

input_file = sys.argv[1]

def part1_run_commands(commands):
    x = 0
    depth = 0
    for (opcode, amount) in commands:
        if (opcode == "forward"):
            x += amount
        elif (opcode == "down"):
            depth += amount
        elif  (opcode == "up"):
            depth -= amount
    return (x, depth)

def part2_run_commands(commands):
    x = 0
    depth = 0
    aim = 0
    for (opcode, amount) in commands:
        if (opcode == "forward"):
            x += amount
            depth += aim * amount
        elif (opcode == "down"):
            aim += amount
        elif  (opcode == "up"):
            aim -= amount
    return (x, depth)


with open(input_file, newline='',encoding='utf-8') as file:

    lines = file.readlines()
    commands = []
    for line in lines:
        command = line.split(" ")
        opcode = command[0]
        amount = int(command[1])
        commands.append((opcode, amount))

    (x, depth) = part1_run_commands(commands)

    print("What do you get if you multiply your final horizontal position by your final depth?: {0}".format(x*depth))

    (x, depth) = part2_run_commands(commands)

    print("What do you get if you multiply your final horizontal position by your final depth?: {0}".format(x*depth))
    