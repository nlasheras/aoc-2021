""" https://adventofcode.com/2021/day/12 """

from collections import defaultdict
import re

class Graph:
    """A graph implemented with a dictionary of adjacency between nodes"""
    def __init__(self):
        self.adjacency = defaultdict(lambda: [])

    def add_edge(self, start, end):
        self.adjacency[start] += [end]
        self.adjacency[end] += [start]

    def neighbors(self, node):
        return sorted(self.adjacency[node])

    @staticmethod
    def from_file(filename):
        with open(filename, "r", encoding="utf-8") as file:
            ret = Graph()
            edge_re = re.compile(r"(\w+)-(\w+)")
            for _l in file.readlines():
                if match := edge_re.search(_l):
                    ret.add_edge(match.group(1), match.group(2))
            return ret

def find_paths(graph, nodes, can_be_in_path):
    """This function implements a recursive DF traversal on the graph checking the neighbors
    with a function so we can re-use it for both parts"""
    paths = []
    for node in graph.neighbors(nodes[-1]):
        if node == 'end':
            paths += [nodes + [node]]
        elif not can_be_in_path(tuple(nodes), node):
            continue
        else:
            paths += find_paths(graph, nodes + [node], can_be_in_path)
    return paths


def part1_count_paths(filename):
    caves = Graph.from_file(filename)

    def part1_cond(path, node):
        if node.islower() and node in path:
            return False
        return True

    paths = find_paths(caves, ["start"], part1_cond)

    print(f"How many paths through this cave system are there that visit small caves at most once? {len(paths)}")

def part2_visit_small_caves_twice(filename):
    caves = Graph.from_file(filename)

    def part2_cond(path, node):
        if node.isupper():
            return True
        if node == "start" and node in path:
            return False # start can only be visited once
        if not node in path:
            return True

        count_node = sum([1 for e in path if e == node])
        if count_node > 1:
            return False

        counts = defaultdict(int)
        for _n in path:
            if _n.islower():
                counts[_n] += 1
        counts[node] += 1 # assume its in path

        caves_visited_twice = sum([1 for e in counts.values() if e >= 2])
        return  caves_visited_twice <= 1

    paths = find_paths(caves, ["start"], part2_cond)
    print(f"How many paths through this cave system are there that visit small caves at most once? {len(paths)}")

if __name__ == '__main__':
    part1_count_paths("input12_test2.txt")
    part1_count_paths("input12.txt")

    part2_visit_small_caves_twice("input12_test1.txt")
    part2_visit_small_caves_twice("input12_test2.txt")
    part2_visit_small_caves_twice("input12_test3.txt")
    part2_visit_small_caves_twice("input12.txt")
