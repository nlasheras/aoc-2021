# https://adventofcode.com/2021/day/12

from collections import defaultdict

class Graph:
    def __init__(self):
        self.adjacency = defaultdict(lambda: [])
    
    def add_edge(self, start, end):
        self.adjacency[start] += [end]
        self.adjacency[end] += [start]

    def neighbors(self, node):
        return sorted(self.adjacency[node])

import re
def read_input(filename):
    with open(filename, "r") as file:
        g = Graph()
        lines = file.readlines()
        r = re.compile("(\w+)-(\w+)")
        for l in lines:
            if match := r.search(l):
                g.add_edge(match.group(1), match.group(2))
        return g

def find_paths(g, nodes, can_be_in_path):
    paths = []
    for n in g.neighbors(nodes[-1]):
        if n == 'end':
            paths += [nodes + [n]]
        elif not can_be_in_path(nodes, n):
            continue 
        else:
            paths += find_paths(g, nodes + [n], can_be_in_path)
    return paths
    

def part1_count_paths(filename):
    g = read_input(filename)
    
    def part1_cond(path, n):
        if n.islower() and n in path:
            return False
        return True

    paths = find_paths(g, ["start"], part1_cond)

    print(f"How many paths through this cave system are there that visit small caves at most once? {len(paths)}")

def part2_visit_small_caves_twice(filename):
    g = read_input(filename)
    
    def part2_cond(path, n):
        if n.isupper():
            return True
        elif n == "start" and n in path:
            return False # start can only be visited once
        elif not n in path:
            return True

        counts = {n: sum([1 for e in path if e == n]) for n in path if n.islower()}
        counts[n] += 1 # assume it's in path

        if counts[n] > 2: # a single node can be visited at most twice
            return False

        s = sum([1 for e in counts.values() if e >= 2])
        return  s <= 1

    paths = find_paths(g, ["start"], part2_cond)
    print(f"How many paths through this cave system are there that visit small caves at most once? {len(paths)}")

if __name__ == '__main__':
    part1_count_paths("input12_test2.txt")
    part1_count_paths("input12.txt")
    
    part2_visit_small_caves_twice("input12_test1.txt")
    part2_visit_small_caves_twice("input12_test2.txt")
    part2_visit_small_caves_twice("input12_test3.txt")
    part2_visit_small_caves_twice("input12.txt")
