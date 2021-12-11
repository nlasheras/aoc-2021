# https://adventofcode.com/2021/day/11

class Grid:
    def __init__(self, filename):
        with open(filename, "r", encoding='utf-8') as file:
            lines = [l.rstrip() for l in file.readlines()]
            self.rows = len(lines)
            self.cols = len(lines[0])
            self.cells = []
            for l in lines:
                self.cells += [int(c) for c in l]

    def get_idx(self, p):
        if 0 <= p[0] < self.cols and 0 <= p[1] < self.rows:
            return p[0] + p[1]*self.cols

    def get_pos(self, idx):
        row = idx // self.cols
        col = idx % self.cols
        return (col, row)

    def step(self):
        flashed = [False] * self.rows * self.cols

        def flash_cell(idx):
            neighbors = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            flashed[idx] = True
            pi = self.get_pos(idx)
            adjacent_indexes = list(filter(lambda x: x != None, 
                                    [self.get_idx((pi[0] + delta[0], pi[1] + delta[1])) 
                                        for delta in neighbors]))
            for adj_i in adjacent_indexes:
                if not flashed[adj_i]: 
                    self.cells[adj_i] += 1 

        def check_flash_iteration():
            count = 0
            for i in range(self.rows * self.cols):
                if self.cells[i] > 9 and not flashed[i]:
                    flash_cell(i)
                    count += 1
            return count

        # add 1 to the octopus energy
        self.cells = list(map(lambda x: x + 1, self.cells))

        # keep checking for flash until no cell has flashed
        count = 0
        while (c := check_flash_iteration()) > 0:
            count += c

        # after all the flashing has happened we set the flashing octopus to 0
        self.cells = [0 if v > 9 else v for v in self.cells]

        return count

    def render(self, highlight = []):

        def get_str(i):
            return str(self.cells[i])

        ENDC = '\033[0m'
        BOLD = '\033[1m'

        render = ""
        for y in range(self.rows):
            for x in range(self.cols):
                idx = self.get_idx((x, y))
                cell_str = get_str(idx)
                if idx in highlight:
                    cell_str = BOLD + cell_str + ENDC
                render += cell_str
            render += "\n" if y < self.rows - 1 else ""
        return render

    def print(self, hightlight = []):
        print(self.render())


def part1_count_flashes(input):
    g = Grid(input)
    steps = 100

    sum = 0
    for i in range(1, steps + 1):
        sum += g.step()
    
    print(f"How many total flashes are there after {steps} steps? {sum}")

def part2_find_synchronize_step(input):
    g = Grid(input)

    total_octopuses = g.cols * g.rows

    flashes = 0
    i = 0
    while flashes != total_octopuses:
        i += 1
        flashes = g.step()
    
    print(f"Octopuses synchronize after step {i}")

if __name__ == '__main__':
    part1_count_flashes("input11_test.txt")
    part1_count_flashes("input11.txt")

    part2_find_synchronize_step("input11_test.txt")
    part2_find_synchronize_step("input11.txt")