# https://adventofcode.com/2021/day/14

import re
from collections import defaultdict

def read_input(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        template = lines[0].rstrip()
        rules = defaultdict(dict)
        rule_re = re.compile("(\w)(\w) -> (\w)")
        for l in lines[2:]:
            if match := rule_re.match(l):
                rules[match.group(1)][match.group(2)] = match.group(3) 
                
    return (template, rules)

def expand(polymer, pair_insertion_dict):
    new_polymer = ""
    for pair in zip(polymer, polymer[1:]):
        new_polymer += pair[0]
        if pair[1] in pair_insertion_dict[pair[0]]:
            new_polymer += pair_insertion_dict[pair[0]][pair[1]]
    new_polymer += polymer[-1]
    return new_polymer

def expand_and_print_difference(filename, steps, print_steps = 0):
    polymer, pair_insertion_dict = read_input(filename)
    for i in range(steps):
        polymer = expand(polymer, pair_insertion_dict)
        if i < print_steps: 
            print(f"After step {i+1}: {polymer}")
            counts = sorted({ c: polymer.count(c) for c in polymer }.items(), key = lambda p: p[1], reverse=True)
            print(counts)

    counts = sorted({ c: polymer.count(c) for c in polymer }.items(), key = lambda p: p[1], reverse=True)
    print(f"What do you get if you take the quantity of the most common element and subtract the quantity of the least common element? {counts[0][1] - counts[-1][1]}")

def expand_pairs(filename, steps, print_steps = 0):
    polymer_string, pair_insertion_dict = read_input(filename)
    pairs = { p: polymer_string.count("".join(p)) for p in zip(polymer_string, polymer_string[1:]) }
    pairs[(polymer_string[-1], "")] = 1

    for i in range(steps):
        new_pairs = defaultdict(int)
        for p,c in pairs.items():
            if p[1] in pair_insertion_dict[p[0]]:
                ic = pair_insertion_dict[p[0]][p[1]]
                new_pairs[(p[0], ic)] += c
                new_pairs[(ic, p[1])] += c
            else:
                new_pairs[p] = c
        pairs = new_pairs

        if (i < print_steps):        
            counts = defaultdict(int)
            for i in pairs:
                counts[i[0]] += pairs[i]
            counts = sorted(counts.items(), key = lambda p: p[1], reverse=True)
            print(counts)

    counts = defaultdict(int)
    for i in pairs:
        counts[i[0]] += pairs[i]
    counts = sorted(counts.items(), key = lambda p: p[1], reverse=True)

    #print(counts)
    print(f"What do you get if you take the quantity of the most common element and subtract the quantity of the least common element? {counts[0][1] - counts[-1][1]}")

def part1(filename):
    #expand_and_print_difference(filename, 10, 0)
    expand_pairs(filename, 10, 0)

def part2(filename):
    expand_pairs(filename, 40, 0)

if __name__ == '__main__':
    part1("input14_test.txt")
    part1("input14.txt")
    
    print("\n", end='')
    
    part2("input14_test.txt")
    part2("input14.txt")
