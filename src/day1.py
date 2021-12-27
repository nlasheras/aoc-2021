""" https://adventofcode.com/2021/day/1 """

import sys

def part1_count_increases(measurements):
    """Count increases of a measure with the next."""
    windows = zip(measurements[1:], measurements[:-1])
    increases = filter(lambda w: w[0] > w[1], windows)
    return len(list(increases))

def part2_count_using_sliding_window(measurements):
    """Count increases using a sliding windows of 3 measurements."""
    windows = zip(measurements, measurements[1:], measurements[2:])
    sums = list(map(lambda t: t[0] + t[1] + t[2], windows))
    return part1_count_increases(sums)

if __name__ == '__main__':
    INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input1.txt"

    with open(INPUT_FILE, newline='',encoding='utf-8') as file:
        report = [int(line) for line in file.readlines()]

        solution1 = part1_count_increases(report)
        print(f"How many measurements are larger than the previous measurement?: {solution1}")

        solution2 = part2_count_using_sliding_window(report)
        print(f"How many sums are larger than the previous sum?: {solution2}")
