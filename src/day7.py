""" https://adventofcode.com/2021/day/7 """

import sys
from functools import reduce

def binary_search(low, high, cost_func):
    if low == high: # base case
        return low

    mid = (high + low) // 2
    mid_cost = cost_func(mid)

    if cost_func(mid+1) > mid_cost:
        return binary_search(low, mid, cost_func)
    if cost_func(mid+1) < mid_cost:
        return binary_search(mid+1, high, cost_func)
    return mid

def part1_align_crabs(crabs):
    max_x = reduce(max, crabs)

    def fuel_cost(idx):
        return sum([abs(idx - c) for c in crabs])

    pos = binary_search(0, max_x, fuel_cost)
    return fuel_cost(pos)

def part2_align_crabs(crabs):
    max_x = reduce(max, crabs)

    def fuel_cost(idx):
        """For part 2 the cost follows the triangular number sequence"""
        def __triangular__(_n: int):
            return sum(range(1, _n+1))

        return sum([__triangular__(abs(idx - c)) for c in crabs])

    pos = binary_search(0, max_x, fuel_cost)
    return fuel_cost(pos)

if __name__ == '__main__':
    example = [int(n) for n in "16,1,2,0,4,2,7,1,2,14".split(",")]
    cost = part1_align_crabs(example)
    print(f"How much fuel must they spend to align to that position? {cost}")
    cost = part2_align_crabs(example)
    print(f"How much fuel must they spend to align to that position? {cost}")

    INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input7.txt"
    with open(INPUT_FILE, newline='',encoding='utf-8') as file:
        input_crabs = [int(n) for n in file.readlines()[0].split(",")]
        cost = part1_align_crabs(input_crabs)
        print(f"How much fuel must they spend to align to that position? {cost}")
        cost = part2_align_crabs(input_crabs)
        print(f"How much fuel must they spend to align to that position? {cost}")
