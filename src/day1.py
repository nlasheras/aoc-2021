## https://adventofcode.com/2021/day/1

def part1_count_increases(measurements):
    windows = zip(measurements[1:], measurements[:-1])
    increases = filter(lambda w: w[0] > w[1], windows)
    return len(list(increases))

def part2_count_using_sliding_window(measurements):
    windows = zip(measurements, measurements[1:], measurements[2:])
    sums = list(map(lambda t: t[0] + t[1] + t[2], windows))
    return part1_count_increases(sums)

import sys
input_file = sys.argv[1] if len(sys.argv) > 1 else "input1.txt" 

with open(input_file, newline='',encoding='utf-8') as file:
    measurements = [int(line) for line in file.readlines()]

    solution1 = part1_count_increases(measurements)
    print(f"How many measurements are larger than the previous measurement?: {solution1}")

    solution2 = part2_count_using_sliding_window(measurements)
    print(f"How many sums are larger than the previous sum?: {solution2}")