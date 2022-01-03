""" https://adventofcode.com/2021/day/14 """

import re
from collections import defaultdict

def read_input(filename):
    """Return a tuple with the polymer starting template and the rules as dict of dicts.
    This pair insertion dict has the first key as the first member of the pair and then a
    dict of all the second characters that have an expansion"""
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        template = lines[0].rstrip()
        rules = defaultdict(dict)
        rule_re = re.compile(r"(\w)(\w) -> (\w)")
        for line in lines[2:]:
            if match := rule_re.match(line):
                rules[match.group(1)][match.group(2)] = match.group(3)

    return (template, rules)

def expand(polymer, pair_insertion_dict):
    """Expand a polymer once using the dict"""
    new_polymer = ""
    for pair in zip(polymer, polymer[1:]):
        new_polymer += pair[0]
        if pair[1] in pair_insertion_dict[pair[0]]:
            new_polymer += pair_insertion_dict[pair[0]][pair[1]]
    new_polymer += polymer[-1]
    return new_polymer

def count_elements(_polymer):
    """Return a list of the polymer elements with the tuples sorted by count descending"""
    count_dicts = { c: _polymer.count(c) for c in _polymer }
    return sorted(count_dicts.items(), key = lambda p: p[1], reverse=True)

def expand_and_print_difference(filename, steps, print_steps = 0):
    polymer, pair_insertion_dict = read_input(filename)
    for i in range(steps):
        polymer = expand(polymer, pair_insertion_dict)
        if i < print_steps:
            print(f"After step {i+1}: {polymer}")
            print(count_elements(polymer))

    counts = count_elements(polymer)
    most_common_count = counts[0][1]
    least_common_count = counts[-1][1]
    part1_result = most_common_count - least_common_count
    print(f"What do you get if you take the quantity of the most common element and subtract the quantity of the least common element? {part1_result}")

def expand_pairs(filename, steps, print_steps = 0):
    """Since expanding the polymer 40 times would require too much memory, this implementtion
    just counts how many of each pair we have in the polymer at every step"""
    polymer_string, pair_insertion_dict = read_input(filename)
    pairs = { p: polymer_string.count("".join(p)) for p in zip(polymer_string, polymer_string[1:]) }
    pairs[(polymer_string[-1], "")] = 1

    def counts_from_pairs(_pairs):
        """Since pairs is each element with the next one, we just count the apparitions once,
        when they are the first element in the pair"""
        counts = defaultdict(int)
        for _p in _pairs:
            counts[_p[0]] += pairs[_p]
        return sorted(counts.items(), key = lambda p: p[1], reverse=True)

    for i in range(steps):
        new_pairs = defaultdict(int)
        for pair, count in pairs.items():
            if pair[1] in pair_insertion_dict[pair[0]]:
                insert_char = pair_insertion_dict[pair[0]][pair[1]]
                new_pairs[(pair[0], insert_char)] += count
                new_pairs[(insert_char, pair[1])] += count
            else:
                new_pairs[pair] = count
        pairs = new_pairs

        if i < print_steps:
            print(counts_from_pairs(pairs))

    counts = counts_from_pairs(pairs)
    part2_result = counts[0][1] - counts[-1][1]
    print(f"What do you get if you take the quantity of the most common element and subtract the quantity of the least common element? {part2_result}")

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
