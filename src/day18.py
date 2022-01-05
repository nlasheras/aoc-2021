# https://adventofcode.com/2021/day/18

class TreeNode:
    def __init__(self, parent = None, value = None):
        self.parent = parent
        self.left = None
        self.right = None
        self.value = value
        self.__num_leaves = -1

    def is_tree(self):
        return self.left and self.right

    def __repr__(self) -> str:
        if self.left and self.right: return f"[{self.left},{self.right}]"
        else: return str(self.value) # leaf node

    def __copy__(self):
        n = TreeNode()
        if self.right:
            n.right = copy(self.right)
            n.right.parent = n
        if self.left:
            n.left = copy(self.left)
            n.left.parent = n
        n.value = self.value
        return n

    def depth(self):
        if self.left and self.right: return 1 + max(self.left.depth(), self.right.depth())
        else: return 0

    def swap(self, old, new):
        new.parent = self
        if self.right == old: self.right = new
        elif self.left == old: self.left = new
        self.__invalidate_count__()

    def is_root(self):
        return self.parent is None

    def get_root(self):
        if self.is_root(): return self
        else: return self.parent.get_root()

    def num_leaves(self):
        if self.__num_leaves == -1:
            self.__num_leaves = self.__count_leaves__()
        return self.__num_leaves

    def __count_leaves__(self):
        if not self.is_tree():
            return 1
        return self.left.num_leaves() + self.right.num_leaves()

    def __invalidate_count__(self):
        self.__num_leaves = -1
        if self.parent: self.parent.__invalidate_count__()

    def get_idx(self, target):
        assert(not target.is_tree())
        idx = 0
        current = target
        while (current.parent != None):
            if current == current.parent.right:
                idx += current.parent.left.num_leaves()
            current = current.parent
        return idx

    def get_node_by_idx(self, target_idx):
        if not self.is_tree():
            if target_idx == 0: return self
            else: return None
        left_count = self.left.num_leaves()
        if target_idx >= left_count:
            return self.right.get_node_by_idx(target_idx - left_count)
        else:
            return self.left.get_node_by_idx(target_idx)

def parse_numbers(string):
    def __parse_recursive__(string):
        count = 0
        if string[count] == '[':
            t = TreeNode()
            v, parsed_count = __parse_recursive__(string[1:])
            count += parsed_count + 1
            if string[count] == ",":
                t.left = v
                t.right, parsed_count = __parse_recursive__(string[count+1:])
                count += parsed_count + 1
            if string[count] == ']':
                count += 1
            t.left.parent = t
            t.right.parent = t
            return t, count
        else:
            t = TreeNode()
            t.value = 0
            c = string[count]
            if c.isdigit():
                t.value = t.value*10 + int(c)
                count += 1
            return t, count
    ret, parsed = __parse_recursive__(string)
    assert(parsed == len(string))
    return ret

def add_nodes(n1: TreeNode, n2: TreeNode):
    t = TreeNode()
    t.left = n1
    t.left.parent = t
    t.right = n2
    t.right.parent = t
    return t

def explode(t, depth = 0):
    if t.left and explode(t.left, depth + 1):
        return True
    if depth == 4 and t.is_tree():
        old = t
        root = t.get_root()
        left_idx = root.get_idx(t.left)
        left_node = root.get_node_by_idx(left_idx - 1)

        if left_node: left_node.value += t.left.value
        right_node = root.get_node_by_idx(left_idx + 2)
        if right_node: right_node.value += t.right.value
        new = TreeNode(old.parent, 0)
        t.parent.swap(old, new)
        return True
    if t.right and explode(t.right, depth + 1):
        return True
    return False

import math
def split(t):
    if t.left and split(t.left): return True
    if t.value and t.value >= 10:
        split_node = TreeNode()
        split_node.left = TreeNode(split_node, math.floor(t.value / 2))
        split_node.right = TreeNode(split_node, math.ceil(t.value / 2))
        t.parent.swap(t, split_node)
        return True
    if t.right and split(t.right): return True

def magnitude(t):
    if t.is_tree(): return 3*magnitude(t.left) + 2*magnitude(t.right)
    else: return t.value

from copy import copy
def snailfish_add(n1, n2):
    result = add_nodes(copy(n1), copy(n2))
    should_continue = True
    while should_continue:
        if not explode(result):
            should_continue = split(result)
    return result

def parse_input(filename):
    with open(filename, "r") as file:
        return [parse_numbers(line.rstrip()) for line in file.readlines()]

from functools import reduce
def part1(filename):
    numbers = parse_input(filename)
    sum = reduce(snailfish_add, numbers)
    print(f"What is the magnitude of the final sum? {magnitude(sum)}")

from itertools import permutations
def part2(filename):
    numbers = parse_input(filename)
    magnitudes = map(lambda p: magnitude(snailfish_add(p[0], p[1])), permutations(numbers, 2))
    print(f"What is the largest magnitude of any sum of two different snailfish numbers from the homework assignment? {max(magnitudes)}")

part1("input18_test.txt")
part1("input18.txt")

print("\n", end="")
part2("input18_test.txt")
part2("input18.txt")