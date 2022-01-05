"""" https://adventofcode.com/2021/day/18 """

from copy import copy
from functools import reduce
from itertools import permutations
from typing import List
import math

class TreeNode:
    """I will model the snailfish numbers as a tree"""
    def __init__(self, parent = None, value = None):
        self.parent = parent
        self.left = None
        self.right = None
        self.value = value
        self.__num_leaves = None

    def is_tree(self):
        """Leaf nodes only use the value property"""
        return self.left or self.right

    def __repr__(self) -> str:
        if self.is_tree():
            return f"[{self.left},{self.right}]"
        return str(self.value) # leaf node

    def __copy__(self):
        copied = TreeNode()
        if self.right:
            copied.right = copy(self.right)
            copied.right.parent = copied
        if self.left:
            copied.left = copy(self.left)
            copied.left.parent = copied
        copied.value = self.value
        return copied

    def depth(self):
        if self.left and self.right:
            return 1 + max(self.left.depth(), self.right.depth())
        return 0

    def swap(self, old, new):
        """Swap one of the branches of the node by another tree"""
        new.parent = self
        if self.right == old:
            self.right = new
        elif self.left == old:
            self.left = new
        self.__invalidate_count__()

    def is_root(self):
        return self.parent is None

    def get_root(self):
        if self.is_root():
            return self
        return self.parent.get_root()

    def num_leaves(self):
        """This method memoizes the count since its a heavily used method to traverse
        the tree"""
        if self.__num_leaves is None:
            self.__num_leaves = self.__count_leaves__()
        return self.__num_leaves

    def __count_leaves__(self):
        if not self.is_tree():
            return 1
        return self.left.num_leaves() + self.right.num_leaves()

    def __invalidate_count__(self):
        self.__num_leaves = None
        # when a node memoization gets invalidated, we need to invalidate up until
        # the root
        if self.parent:
            self.parent.__invalidate_count__()

    def get_idx(self):
        """Gets the index of a given leaf node. That index is equal to the amount of
        leaves it has to the left from the root node"""
        assert not self.is_tree() # only leaf nodes have index
        idx = 0
        current = self
        while current.parent:
            if current == current.parent.right:
                idx += current.parent.left.num_leaves()
            current = current.parent
        return idx

    def get_node_by_idx(self, target_idx):
        """Traverse the tree and get a given node. If node doesn't exist return None.
        This is useful to allow accessing nodes -1 or n+1"""
        if not self.is_tree():
            if target_idx == 0:
                return self
            return None

        left_count = self.left.num_leaves()
        if target_idx >= left_count:
            return self.right.get_node_by_idx(target_idx - left_count)
        return self.left.get_node_by_idx(target_idx)

def parse_numbers(input_string) -> List[TreeNode]:
    def __parse_recursive__(string):
        count = 0
        if string[count] == '[':
            # tree node, parse left and then the right branch
            tree = TreeNode()
            tree.left, parsed_count = __parse_recursive__(string[1:])
            count += parsed_count + 1
            assert string[count] == ','
            if string[count] == ",":
                tree.right, parsed_count = __parse_recursive__(string[count+1:])
                count += parsed_count + 1 # skip also the ','
            assert string[count] == ']'
            if string[count] == ']':
                count += 1
            # set parent to the parsed branches
            tree.left.parent = tree
            tree.right.parent = tree
            return tree, count
        else:
            # parse the number as a leaf node
            tree = TreeNode()
            tree.value = 0
            while string[count].isdigit():
                tree.value = tree.value*10 + int(string[count])
                count += 1
            return tree, count
    ret, parsed_chars = __parse_recursive__(input_string)
    assert parsed_chars == len(input_string)
    return ret

def add_nodes(node1: TreeNode, node2: TreeNode):
    """The sum of two trees is a new tree where each tree is one of the
    branches"""
    sum_node = TreeNode()
    sum_node.left = copy(node1)
    sum_node.left.parent = sum_node
    sum_node.right = copy(node2)
    sum_node.right.parent = sum_node
    return sum_node

def explode(tree, depth = 0):
    """Keep exploding the numbers from the left to the right. When exploding
    the left value is added to the node to the left and the right value is
    added to the node to the right. The exploded node is replaced by a leaf
    node with value 0"""
    if tree.left and explode(tree.left, depth + 1):
        return True
    if depth == 4 and tree.is_tree():
        # when exploding we a node we require two leaf nodes
        assert not tree.left.is_tree()
        assert not tree.right.is_tree()
        exploded = tree
        root = tree.get_root()

        left_leaf_idx = tree.left.get_idx()
        if left_node := root.get_node_by_idx(left_leaf_idx - 1):
            left_node.value += tree.left.value

        if right_node := root.get_node_by_idx(left_leaf_idx + 2):
            right_node.value += tree.right.value

        new = TreeNode(exploded.parent, 0)
        exploded.parent.swap(exploded, new)
        return True
    if tree.right and explode(tree.right, depth + 1):
        return True
    return False

def split(tree):
    """When a regular number is bigger than 10 we replace it with a new Tree where
    the left one is the half rounded down and the right one the half rounding up"""
    if tree.left and split(tree.left):
        return True
    if tree.value and tree.value >= 10:
        split_node = TreeNode()
        split_node.left = TreeNode(split_node, math.floor(tree.value / 2))
        split_node.right = TreeNode(split_node, math.ceil(tree.value / 2))
        tree.parent.swap(tree, split_node)
        return True
    if tree.right and split(tree.right):
        return True
    return False

def magnitude(tree):
    if tree.is_tree():
        return 3*magnitude(tree.left) + 2*magnitude(tree.right)
    return tree.value

def snailfish_add(node1, node2):
    result = add_nodes(node1, node2)
    should_reduce = True
    while should_reduce:
        # at most one action applies, we first apply all the explode before we start spliting,
        # and after any split we check for any split needed. We keep reducing the number until no
        # explode and split are required
        if not explode(result):
            should_reduce = split(result)
    return result

def parse_input(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return [parse_numbers(line.rstrip()) for line in file.readlines()]

def part1(filename):
    numbers = parse_input(filename)
    final_sum = reduce(snailfish_add, numbers)
    print(f"What is the magnitude of the final sum? {magnitude(final_sum)}")

def part2(filename):
    numbers = parse_input(filename)
    magnitudes = map(lambda p: magnitude(snailfish_add(p[0], p[1])), permutations(numbers, 2))
    print(f"What is the largest magnitude of any sum of two different snailfish numbers from the homework assignment? {max(magnitudes)}")

if __name__ == '__main__':
    part1("input18_test.txt")
    part1("input18.txt")

    print("\n", end="")
    part2("input18_test.txt")
    part2("input18.txt")
