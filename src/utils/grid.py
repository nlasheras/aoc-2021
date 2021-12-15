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

    def neighbors(self, p):
        valid = []
        for delta in [(1,0), (0,1), (-1, 0), (0, -1)]:
            pos = (p[0] + delta[0], p[1] + delta[1])
            if (pos[0] >= 0 and pos[0] < self.cols and
                pos[1] >= 0 and pos[1] < self.rows):
                valid.append(pos)
        return valid

    def render(self, highlight = []):

        def __get_str__(i):
            return str(self.cells[i])

        ENDC = '\033[0m'
        BOLD = '\033[1m'
        YELLOW = '\033[93m'

        render = ""
        for y in range(self.rows):
            for x in range(self.cols):
                idx = self.get_idx((x, y))
                cell_str = __get_str__(idx)
                if idx in highlight:
                    cell_str = YELLOW + BOLD + cell_str + ENDC
                render += cell_str
            render += "\n" if y < self.rows - 1 else ""
        return render

    def print(self, highlight = []):
        print(self.render(highlight))