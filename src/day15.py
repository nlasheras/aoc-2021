""" https://adventofcode.com/2021/day/15 """

from collections import defaultdict
from queue import PriorityQueue
from utils import Grid

def find_path(grid, start, goal):
    """ implement A* """

    # open set is a PriorityQueue ordered by fScore
    open_set = PriorityQueue()
    open_set.put((0, start))
    # we use the closed set to avoid processing nodes multiple times
    closed_set = set()

    came_from = {} # empty map

    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0

    def h_func(pos):
        return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])

    def g_func(pos):
        return grid.get_value(pos)

    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = h_func(start)

    while not open_set.empty():
        # get the element in open_set with smallest fScore
        _, current = open_set.get()
        if current in closed_set:
            continue

        closed_set.add(current)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path = [current] + path

            return True, path[1:]

        for neighbor in grid.neighbors(current):
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + g_func(neighbor)
            if tentative_g_score < g_score[neighbor]:
                # this is the better path
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h_func(neighbor)
                open_set.put((f_score[neighbor], neighbor))

    return False, []

def find_path_in_grid(grid, print_path):
    found, path = find_path(grid, (0,0), (grid.cols-1, grid.rows-1))
    if found:
        indexes = [grid.get_idx(p) for p in path]
        if print_path:
            grid.print(indexes)
        risks = [grid.cells[i] for i in indexes]
        print(f"What is the lowest total risk of any path from the top left to the bottom right? {sum(risks)}")

def part1(filename, print_path = False):
    grid = Grid.from_file(filename)
    find_path_in_grid(grid, print_path)

def part2(filename, print_path = False):
    grid = Grid(filename)

    # generate the new grid
    new_rows = grid.rows * 5
    new_cols = grid.cols * 5
    new_cells = [0] * new_cols * new_rows
    for y in range(new_rows):
        for x in range(new_cols):
            source_x = x % grid.cols
            source_y = y % grid.rows
            original_risk = grid.get_value((source_x, source_y))
            tile_x = x // grid.cols
            tile_y = y // grid.rows
            new_risk = original_risk + tile_x + tile_y
            while new_risk > 9:
                new_risk -= 9
            new_cells[x + y*new_cols] = new_risk

    grid.cells = new_cells
    grid.cols = new_cols
    grid.rows = new_rows

    find_path_in_grid(grid, print_path)

if __name__ == '__main__':
    part1("input15_test.txt", True)
    part1("input15.txt")
    part2("input15_test.txt", True)
    part2("input15.txt")
