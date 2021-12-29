""" https://adventofcode.com/2021/day/6 """

import sys

def simulate_1day_reference(fishes):
    new_fishes = [8 for n in fishes if n == 0] # new fishes spawn when counter is 0
    fishes = [i-1 if i>0 else 6 for i in fishes] # after a fish spawn fishes start with timer 6
    return fishes + new_fishes

def simulate_1day_fast(counters):
    """The fastest way to simulate the fishes is using a count of how many fishes
    have each timer value and just using those timers the fishes popping in front of
    the timer array get duplicated both as new fishes with time '8' and increasing
    the value of the '6' counter
    """
    reproducing_fishes, new_counters = counters[0], counters[1:] + [0]
    new_counters[6] += reproducing_fishes
    new_counters[8] = reproducing_fishes
    return new_counters

def simulate_fishes(fishes, days):
    # I build the counters array with space for the 8 timer so I don't need
    # to handle the edge case in the simulate function
    counters = [sum([1 for f in fishes if f == t]) for t in range(9)]
    for _ in range(days):
        counters = simulate_1day_fast(counters)
    return sum(counters)

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input6.txt"
    with open(input_file, newline='',encoding='utf-8') as file:
        fishes = [int(n) for n in file.readlines()[0].split(",")]

        amount = simulate_fishes(fishes, 80)
        print(f"After 80 days = {amount} fishes")

        amount = simulate_fishes(fishes, 256)
        print(f"After 256 days = {amount}")

def print_example():
    fishes = [3,4,3,1,2]

    counters = [sum([1 for f in fishes if f == t]) for t in range(9)]

    for i in range(18):
        fishes = simulate_1day_reference(fishes)
        counters = simulate_1day_fast(counters)
        print(f"After {i+1} day ({len(fishes)}, {sum(counters)}) {fishes}")
    print("\n")

if __name__ == '__main__':
    #print_example()
    main()
