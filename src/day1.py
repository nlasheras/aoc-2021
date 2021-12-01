## https://adventofcode.com/2021/day/1

import sys

input_file = sys.argv[1]

def part1_count_increases(measurements):
    count = 0
    n = len(measurements)
    for i in range(1, n):
        if measurements[i] > measurements[i-1]:
            count += 1
    return count

def part2_count_using_sliding_window(measurements):
    count = 0
    n = len(measurements)

    # using a temp variable to avoid doing the sum twice
    previous_sum = sum(measurements[0:3])
    for i in range(1, n-2):
        current_window = sum(measurements[i:i+3])
        if (current_window > previous_sum):
            count += 1
        previous_sum = current_window
    return count

with open(input_file, newline='',encoding='utf-8') as file:

    # read input
    lines = file.readlines()
    measurements = []
    for line in lines:
        measurements.append(int(line))

    solution1 = part1_count_increases(measurements)
    print("How many measurements are larger than the previous measurement?: {0}".format(solution1))

    solution2 = part2_count_using_sliding_window(measurements)
    print("How many sums are larger than the previous sum?: {0}".format(solution2))