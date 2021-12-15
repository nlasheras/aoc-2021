# https://adventofcode.com/2021/day/15

from utils import Grid
from collections import defaultdict
import math
from functools import reduce
from queue import PriorityQueue

def find_path(grid, start, goal):
    # implement A*

    # open set is a PriorityQueue ordered by fScore
    open_set = PriorityQueue()
    open_set.put((0, start))
    # we use the closed set to avoid processing nodes multiple times
    closed_set = set()

    came_from = {} # empty map

    gScore = defaultdict(lambda: float('inf'))
    gScore[start] = 0

    def h_func(pos):
        return math.fabs(goal[0] - pos[0]) + math.fabs(goal[1] - pos[1])

    def g_func(pos):
        return grid.cells[grid.get_idx(pos)]

    fScore = defaultdict(lambda: float('inf'))
    fScore[start] = h_func(start)

    while not open_set.empty():
        # get the element in open_set with smallest fScore
        _, current = open_set.get()
        if current in closed_set:
            continue

        closed_set.add(current)

        if current == goal:
            path = [current]
            while current in came_from.keys():
                current = came_from[current]
                path = [current] + path

            return True, path[1:]

        for neighbor in grid.neighbors(current):
            if neighbor in closed_set:
                continue
            tentative_gScore = gScore[current] + g_func(neighbor)
            if tentative_gScore < gScore[neighbor]:
                # this is the better path
                came_from[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + h_func(neighbor)
                open_set.put((fScore[neighbor], neighbor))
    
    return False, []

def find_path_in_grid(g, print_path):
    found, path = find_path(g, (0,0), (g.cols-1, g.rows-1))
    if found:
        indexes = [g.get_idx(p) for p in path]
        if print_path: g.print(indexes)
        risks = [g.cells[i] for i in indexes]
        print(f"What is the lowest total risk of any path from the top left to the bottom right? {sum(risks)}")

def part1(filename, print_path = False):
    g = Grid(filename)
    find_path_in_grid(g, print_path)

def part2(filename, print_path = False):
    g = Grid(filename)

    # generate the new grid
    new_rows = g.rows * 5
    new_cols = g.cols * 5
    new_cells = [0] * new_cols * new_rows
    for y in range(new_rows):
        for x in range(new_cols):
            ox = x % g.cols
            oy = y % g.rows
            orisk = g.cells[ox + oy*g.rows]
            tx = x // g.cols
            ty = y // g.rows
            new_risk = orisk + tx + ty
            while new_risk > 9:
                new_risk -= 9
            new_cells[x + y*new_cols] = new_risk
    
    g.cells = new_cells
    g.cols = new_cols
    g.rows = new_rows

    find_path_in_grid(g, print_path)

if __name__ == '__main__':
    part1("input15_test.txt", True)
    part1("input15.txt")
    part2("input15_test.txt", True)
    part2("input15.txt")
