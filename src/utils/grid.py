from itertools import product
from utils.termcolors import TermColors

class Grid:
    """A grid of cells of any type"""
    def __init__(self):
        self.cells = []
        self.rows = 0
        self.cols = 0

    @staticmethod
    def from_file(filename, parse_cell = int):
        """Initialize a grid from a file where every cell is one character of the file"""
        with open(filename, "r", encoding='utf-8') as file:
            grid = Grid()
            lines = [l.rstrip() for l in file.readlines()]
            grid.rows = len(lines)
            grid.cols = len(lines[0])
            for _l in lines:
                grid.cells += [parse_cell(c) for c in _l]
            return grid
        return None

    @staticmethod
    def empty(cols, rows, initial_value = 0):
        """Initialize an empty grid with a starting value"""
        grid = Grid()
        grid.cols = cols
        grid.rows = rows
        grid.cells = [initial_value] * cols * rows
        return grid

    def get_idx(self, pos):
        """Get the index of position pos in the cells array"""
        if 0 <= pos[0] < self.cols and 0 <= pos[1] < self.rows:
            return pos[0] + pos[1]*self.cols
        return None

    def get_pos(self, index):
        """Get the row and column of a given index"""
        row = index // self.cols
        col = index % self.cols
        return (col, row)

    def neighbors(self, pos):
        """Get the neighbor positions of a given position"""
        valid = []
        for delta in [(1,0), (0,1), (-1, 0), (0, -1)]:
            npos = (pos[0] + delta[0], pos[1] + delta[1])
            if (0 <= npos[0] < self.cols and
                0 <= npos[1] < self.rows):
                valid.append(npos)
        return valid

    def positions(self):
        """Return an iterator of position tuples"""
        return product(range(self.cols), range(self.rows))

    def get_value(self, pos):
        """Get the cell of a given position"""
        if 0 <= pos[0] < self.cols and 0 <= pos[1] < self.rows:
            idx = self.get_idx(pos)
            return self.cells[idx]
        return None

    def render(self, highlight = None):
        def __get_str__(i):
            return str(self.cells[i])

        render = ""
        for y in range(self.rows):
            for x in range(self.cols):
                idx = self.get_idx((x, y))
                cell_str = __get_str__(idx)
                if highlight and idx in highlight:
                    cell_str = TermColors.YELLOW + TermColors.BOLD + cell_str + TermColors.ENDC
                render += cell_str
            render += "\n" if y < self.rows - 1 else ""
        return render

    def print(self, highlight = None):
        print(self.render(highlight))
