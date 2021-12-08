from functools import reduce

def binary_search(low, high, cost_func):
    if low == high: # base case
        return low

    mid = (high + low) // 2
    mc = cost_func(mid)

    if cost_func(mid+1) > mc:
        return binary_search(low, mid, cost_func)
    elif cost_func(mid+1) < mc:
        return binary_search(mid+1, high, cost_func)
    else:
        return mid

def part1_align_crabs(crabs):
    max_x = reduce(lambda acc, x: max(acc, x), crabs)

    def fuel_cost(idx):
        return sum([abs(idx - c) for c in crabs])

    pos = binary_search(0, max_x, fuel_cost)
    return fuel_cost(pos)

def part2_align_crabs(crabs):
    max_x = reduce(lambda acc, x: max(acc, x), crabs)

    def fuel_cost(idx):
        return sum([sum(range(1, abs(idx - c)+1)) for c in crabs])

    pos = binary_search(0, max_x, fuel_cost)
    return fuel_cost(pos)

import sys
if __name__ == '__main__':
    example = [int(n) for n in "16,1,2,0,4,2,7,1,2,14".split(",")]
    cost = part1_align_crabs(example)
    print(f"How much fuel must they spend to align to that position? {cost}")
    cost = part2_align_crabs(example)
    print(f"How much fuel must they spend to align to that position? {cost}")

    input_file = sys.argv[1] if len(sys.argv) > 1 else "input7.txt"
    with open(input_file, newline='',encoding='utf-8') as file:
        crabs = [int(n) for n in file.readlines()[0].split(",")]
        cost = part1_align_crabs(crabs)
        print(f"How much fuel must they spend to align to that position? {cost}")
        cost = part2_align_crabs(crabs)
        print(f"How much fuel must they spend to align to that position? {cost}")
  


