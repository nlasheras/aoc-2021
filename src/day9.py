# https://adventofcode.com/2021/day/9

def read_input(filename):
    with open(filename, "r", encoding='utf-8') as file:
        lines = file.readlines()
        grid = [[int(c) for c in l.rstrip()] for l in lines]
        return (grid, (len(grid[0]), len(grid)))

def get_value(input, x, y):
    grid, (cols,rows) = input
    if x >= 0 and x < cols and y >= 0 and y < rows:
        return grid[y][x]

adjacent = [(-1, 0), (0, -1), (1, 0), (0, 1)]

def find_lower_points(input):
    grid, (cols,rows) = input

    lower_points = []
    for y in range(rows):
        for x in range(cols):
            value = get_value(input, x, y)
            adjacent_values = [get_value(input, x + delta[0], y + delta[1]) for delta in adjacent]
            # point needs to be strictly lower than any of their adjacents
            smaller_adjacent = [v for v in adjacent_values if v != None and v <= value]
            if not len(smaller_adjacent):
                lower_points.append((x, y))

    return lower_points

def part1(input):
    lower_points = find_lower_points(input)
    risk = sum([1 + get_value(input, p[0], p[1]) for p in lower_points])
    print(f"What is the sum of the risk levels of all low points on your heightmap? {risk}")

def find_basin(input, lower_point):
    grid = input[0]

    def find_adj(x, y, value):
        adj = [(x + delta[0], y + delta[1]) for delta in adjacent]
        equal_adj = [p for p in adj if get_value(input, p[0], p[1]) == value]
        return equal_adj


    def recursive_find(point, value):
        if (value == 9):
            return [] # Locations of height 9 do not count as being in any basin

        basin = [(point, value)]
        adj = find_adj(point[0], point[1], value + 1)
        for a in adj:
            basin += [p for p in recursive_find(a, value + 1) if not p in basin]
        return basin
    
    basin = recursive_find(lower_point, get_value(input, lower_point[0], lower_point[1]))
    return basin

from functools import reduce

def part2(input):
    lower_points = find_lower_points(input)
    basins = [find_basin(input, p) for p in lower_points]
    top_three = sorted(basins, key = lambda b: len(b), reverse = True)[:3]
    top_three_sizes = [len(b) for b in top_three]
    mult = reduce(lambda acc,x: acc * x, top_three_sizes)
    print(f"What do you get if you multiply together the sizes of the three largest basins?", mult)

input = read_input("input9_test.txt")
part1(input)
part2(input)

input = read_input("input9.txt")
part1(input)
part2(input)

