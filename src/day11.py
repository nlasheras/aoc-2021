# https://adventofcode.com/2021/day/11

from utils import Grid

def octopus_step(grid):
    flashed = [False] * grid.rows * grid.cols

    def flash_cell(idx):
        neighbors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        flashed[idx] = True
        pi = grid.get_pos(idx)
        adjacent_indexes = list(filter(lambda x: x != None, 
                                [grid.get_idx((pi[0] + delta[0], pi[1] + delta[1])) 
                                    for delta in neighbors]))
        for adj_i in adjacent_indexes:
            if not flashed[adj_i]: 
                grid.cells[adj_i] += 1 

    def check_flash_iteration():
        count = 0
        for i in range(grid.rows * grid.cols):
            if grid.cells[i] > 9 and not flashed[i]:
                flash_cell(i)
                count += 1
        return count

    # add 1 to the octopus energy
    grid.cells = list(map(lambda x: x + 1, grid.cells))

    # keep checking for flash until no cell has flashed
    count = 0
    while (c := check_flash_iteration()) > 0:
        count += c

    # after all the flashing has happened we set the flashing octopus to 0
    grid.cells = [0 if v > 9 else v for v in grid.cells]

    return count

def part1_count_flashes(input):
    g = Grid(input)
    steps = 100

    sum = 0
    for i in range(1, steps + 1):
        sum += octopus_step(g)
    
    print(f"How many total flashes are there after {steps} steps? {sum}")

def part2_find_synchronize_step(input):
    g = Grid(input)

    total_octopuses = g.cols * g.rows

    flashes = 0
    i = 0
    while flashes != total_octopuses:
        i += 1
        flashes = octopus_step(g)
    
    print(f"Octopuses synchronize after step {i}")

if __name__ == '__main__':
    part1_count_flashes("input11_test.txt")
    part1_count_flashes("input11.txt")

    part2_find_synchronize_step("input11_test.txt")
    part2_find_synchronize_step("input11.txt")