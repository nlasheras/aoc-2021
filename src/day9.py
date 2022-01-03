""" https://adventofcode.com/2021/day/9 """

from functools import reduce
from operator import mul
from utils import Grid

def find_lower_points(heightmap: Grid):
    """Find the points on the heighbmap that are smaller to all adjacent values"""
    lower_points = []
    for pos in heightmap.positions():
        value = heightmap.get_value(pos)
        adjacent_values = [heightmap.get_value(n) for n in heightmap.neighbors(pos)]
        # point needs to be strictly lower than any of their adjacents
        if all(map(lambda adj, _value = value: adj > _value, adjacent_values)):
            lower_points.append(pos)

    return lower_points

def part1(input_file):
    grid = Grid.from_file(input_file)
    lower_points = find_lower_points(grid)
    risk = sum([1 + grid.get_value(p) for p in lower_points])
    print(f"What is the sum of the risk levels of all low points on your heightmap? {risk}")

def find_basin(heightmap: Grid, lower_point):
    """Find all the points contained on the basin that will flow to a single lower point"""

    def recursive_find(point, basin):
        height = heightmap.get_value(point)
        adjacents = [p for p in heightmap.neighbors(point) if height < heightmap.get_value(p) < 9]
        basin |= set(adjacents)
        for adj in adjacents:
            basin = recursive_find(adj, basin)
        return basin

    basin = recursive_find(lower_point, {lower_point})
    return basin

def part2(input_file):
    heightmap = Grid.from_file(input_file)
    lower_points = find_lower_points(heightmap)
    basins = [find_basin(heightmap, p) for p in lower_points]
    top_three = sorted(basins, key = len, reverse = True)[:3]
    top_three_sizes = [len(b) for b in top_three]
    size_mul = reduce(mul, top_three_sizes)
    print(f"What do you get if you multiply together the sizes of the three largest basins? {size_mul}")

if __name__ == '__main__':
    TEST_INPUT = "input9_test.txt"
    part1(TEST_INPUT)
    part2(TEST_INPUT)

    PUZZLE_INPUT = "input9.txt"
    part1(PUZZLE_INPUT)
    part2(PUZZLE_INPUT)
