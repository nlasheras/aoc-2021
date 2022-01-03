""" https://adventofcode.com/2021/day/11 """

from utils import Grid

def octopus_step(grid):
    flashed = [False] * grid.rows * grid.cols

    def flash_cell(idx):
        neighbors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        flashed[idx] = True
        p_i = grid.get_pos(idx)
        adjacent_indexes = list(filter(lambda x: not x is None,
                                [grid.get_idx((p_i[0] + delta[0], p_i[1] + delta[1]))
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
    while (flashed_it := check_flash_iteration()) > 0:
        count += flashed_it

    # after all the flashing has happened we set the flashing octopus to 0
    grid.cells = [0 if v > 9 else v for v in grid.cells]

    return count

def part1_count_flashes(input_file):
    grid = Grid.from_file(input_file)
    steps = 100

    total_flashes = 0
    for _ in range(1, steps + 1):
        total_flashes += octopus_step(grid)

    print(f"How many total flashes are there after {steps} steps? {total_flashes}")

def part2_find_synchronize_step(input_file):
    grid = Grid.from_file(input_file)

    total_octopuses = grid.cols * grid.rows

    flashes = 0
    i = 0
    while flashes != total_octopuses:
        i += 1
        flashes = octopus_step(grid)

    print(f"Octopuses synchronize after step {i}")

if __name__ == '__main__':
    part1_count_flashes("input11_test.txt")
    part1_count_flashes("input11.txt")

    part2_find_synchronize_step("input11_test.txt")
    part2_find_synchronize_step("input11.txt")
