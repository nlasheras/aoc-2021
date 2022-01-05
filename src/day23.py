""" https://adventofcode.com/2021/day/23 """

from collections import defaultdict
from copy import copy
from functools import cache
from dataclasses import dataclass, field
from queue import PriorityQueue
import sys
from typing import Tuple, List
from utils import Grid, TermColors

destination_columns = { 'A': 3, 'B': 5, 'C': 7, 'D': 9 }
move_cost = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }

## this will be updated on parse_input
POD_TYPES = ('A', 'B', 'C', 'D')
PODS_PER_TYPE = 2
DESTINATION_INDEXES = {} # dict

def char_from_type(_type:int) -> str:
    return chr(65 + _type)

def get_pod_type(idx: int) -> str:
    return char_from_type(idx // PODS_PER_TYPE)

@dataclass(order=False)
class RoomState:
    """Stores the current state of the amphipods in the room. It has a reference
    to the grid map and then the state is the position of each pod and a list of
    pods that have moved"""
    grid: Grid
    pods: Tuple[int] # pos of each amphipod
    moved_pods: List[int] # idx of moving pods

    def __copy__(self) -> 'RoomState':
        return RoomState(self.grid, copy(self.pods), copy(self.moved_pods))

    # I'm using @cache for the get_path function I want
    def __hash__(self) -> int:
        return self.grid.rows * self.grid.cols
    def __eq__(self, __o) -> bool:
        return self.__hash__() == __o.__hash__()

    def is_finished(self):
        """Checks for all pod types if all the pods are in their destination room"""
        for type_ in range(4):
            pods_in_room = sorted(self.pods[PODS_PER_TYPE*type_:PODS_PER_TYPE*(type_+1)])
            correct_pods = DESTINATION_INDEXES[char_from_type(type_)]
            if pods_in_room != correct_pods:
                return False
        return True

    def get_pod_at_pos(self, pos : Tuple[int, int]) -> int:
        """If there is a pod at a given position, returns the index on the pods list, None if there isn't """
        idx = self.grid.get_idx(pos)
        return self.get_pod_at_grid(idx)

    def get_pod_at_grid(self, idx: int):
        """If there is a pod at a given index, returns the index on the pods list, None if there isn't """
        if idx in self.pods:
            return self.pods.index(idx)
        return None

    def render(self):
        """Returns a string with a render of the RoomState that can be printed in the console"""
        render = ""
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                pod = self.get_pod_at_pos((col, row))
                if pod is not None:
                    type_ = pod // PODS_PER_TYPE

                    # check what color to render the amphipod
                    color = None
                    if self.is_done(pod):
                        color = TermColors.MAGENTA
                    elif pod in self.moved_pods:
                        if pod == self.moved_pods[-1]:
                            color = TermColors.RED
                        else:
                            color = TermColors.YELLOW

                    if color:
                        render += color
                    render += char_from_type(type_)
                    if color:
                        render += TermColors.ENDC
                else:
                    value = self.grid.cells[self.grid.get_idx((col, row))]
                    render += value
            render += "\n"
        return render

    @cache
    def get_path(self, from_idx, to_idx):
        """Returns all the positions that an amphipod must cross to reach
        the destination position. Not including the starting tile."""
        fcol, frow = self.grid.get_pos(from_idx)
        dcol, drow = self.grid.get_pos(to_idx)
        dest_x = dcol - fcol
        dest_y = drow - frow

        def sign(value):
            return 1 if value >= 0 else - 1

        path = []
        if frow > 1:
            for i in range(1, abs(dest_y)+1):
                path.append((fcol, frow+i*sign(dest_y)))
            for i in range(1, abs(dest_x)+1):
                path.append((fcol+i*sign(dest_x), drow))
        else:
            for i in range(1, abs(dest_x)+1):
                path.append((fcol+i*sign(dest_x), frow))
            for i in range(1, abs(dest_y)+1):
                path.append((dcol, frow+i*sign(dest_y)))

        return [self.grid.get_idx(p) for p in path]

    @cache
    def get_hallway_moves(self, from_idx):
        """Returns the indices of the valid hallway postions for a move of
        an amphipod in a given position."""
        col, row = self.grid.get_pos(from_idx)
        assert row == 1
        if row == 1:
            moves = []

            if col > 2:
                moves += [(col-2, 1)]
            elif col > 1:
                moves += [(col-1, 1)]

            grid_columns = self.grid.cols
            if col < grid_columns - 3:
                moves += [(col+2, 1)]
            elif col < grid_columns - 2:
                moves += [(col+1, 1)]

            return [self.grid.get_idx(p) for p in moves \
                if p[0] not in destination_columns.values()]
        return []

    def get_top_pod_in_rooms(self):
        """Returns the first pod in a room that wants to move"""
        ret = []
        for room in POD_TYPES:
            for grid_idx in DESTINATION_INDEXES[room]:
                if grid_idx in self.pods:
                    i = self.pods.index(grid_idx)
                    if not self.is_done(i):
                        ret += [i]
                        break
        return ret

    def get_empty_spot_in_room(self, room):
        """Returns the grid index of the first spot in a room where a pod can enter. If
        there is other type of pods in the room, this won't return anything since pods cannot
        return yet"""
        if room in DESTINATION_INDEXES:
            indexes = DESTINATION_INDEXES[room]
            for grid_idx in reversed(indexes):
                if grid_idx in self.pods:
                    if not self.is_done(self.pods.index(grid_idx)):
                        return None # cannot go back to the room yet
                else:
                    return grid_idx
        return None

    def is_done(self, idx):
        """Checks if the given pod needs to move in this state. A pod will need to move if
        it is in a different room or some amphipod under it needs to move."""
        grid_idx = self.pods[idx]
        col, row = self.grid.get_pos(grid_idx)
        type_ = self.pods.index(grid_idx) // PODS_PER_TYPE
        if col == destination_columns[chr(65 + type_)]:
            if row >= 1:
                for i in range(row+1, self.grid.rows - 1):
                    other = self.get_pod_at_pos((col, i))
                    if other is None:
                        return False
                    other_type = other // PODS_PER_TYPE
                    if type_ != other_type:
                        return False
                return True
        return False

def parse_input(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return __parse_input__(file.readlines())

def __parse_input__(lines):
    # parse file into a grid
    grid = Grid()
    for i,line in enumerate(lines):
        row = list(line.rstrip())
        if i == 0:
            grid.cols = len(row)
        else:
            row += [' '] * (grid.cols - len(row))
        grid.cells += row
    grid.rows = (len(grid.cells) // grid.cols)

    # get the pods into a List of tuples (type, x, y)
    pods = []
    for row in range(grid.rows):
        for col in range(grid.cols):
            idx = grid.get_idx((col, row))
            value = grid.cells[idx]
            if value in POD_TYPES:
                grid.cells[idx] = '.'
                pods.append((value, col, row))

    pods_idx = []
    for type_ in POD_TYPES:
        for pod in pods:
            if pod[0] == type_:
                pods_idx.append(grid.get_idx((pod[1], pod[2])))

    global PODS_PER_TYPE
    PODS_PER_TYPE = len(pods_idx) // 4
    assert len(pods_idx) % PODS_PER_TYPE == 0

    global DESTINATION_INDEXES
    DESTINATION_INDEXES = {}
    for type_ in POD_TYPES:
        dest = []
        for i in range(2, 2+PODS_PER_TYPE):
            pos = (destination_columns[type_], i)
            dest += [grid.get_idx(pos)]
        DESTINATION_INDEXES[type_] = dest

    return RoomState(grid, tuple(pods_idx), [])

def mhd(pos1, pos2):
    """Return Manhattan distance between two given positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def is_path_free(current: RoomState, from_idx, to_idx):
    """Checks if an amphipod can move between two given positions in the grid"""
    for idx in current.get_path(from_idx, to_idx):
        if idx in current.pods:
            return False
    return True

def get_moves(current: RoomState):
    """Get all moves that can be done from a given RoomState"""
    moves = []

    for pod in reversed(current.moved_pods):
        if current.is_done(pod):
            continue
        if pod == current.moved_pods[-1]:
            # do moves por current moving pod
            p_pos = current.pods[pod]
            moves += [(pod, idx) for idx in current.get_hallway_moves(p_pos)]

        type_ = get_pod_type(pod)
        empty_spot_idx = current.get_empty_spot_in_room(type_)
        if empty_spot_idx:
            moves += [(pod, empty_spot_idx)]

    for pod in current.get_top_pod_in_rooms():
        assert not pod in current.moved_pods
        p_pos = current.pods[pod]
        col, _ = current.grid.get_pos(p_pos)
        out_pos = [(col-1, 1), (col+1, 1)]
        for pos in out_pos:
            out_idx = current.grid.get_idx(pos)
            moves += [(pod, out_idx)]

    # translate moves tuples (pod, grid_idx) into Move
    ret = []
    for pod, dest_idx in moves:
        from_idx = current.pods[pod]
        if not is_path_free(current, from_idx, dest_idx):
            continue

        type_ = get_pod_type(pod)
        config = copy(current)
        # replace the index of config.pod[pod]
        config.pods = tuple(dest_idx if p == pod else idx for p, idx in enumerate(current.pods))

        def dist(idx1, idx2):
            return mhd(current.grid.get_pos(idx1), current.grid.get_pos(idx2))

        _cost = move_cost[type_] * dist(from_idx, dest_idx)

        if not pod in config.moved_pods:
            config.moved_pods.append(pod)
        elif pod != config.moved_pods[-1]:
            # whenever a amphipod moves, it moves to the end of moved_pod list
            config.moved_pods.remove(pod)
            config.moved_pods.append(pod)

        ret.append((_cost, config))

    return ret

def find_best_path(starting):
    """Find the best moves using A*"""

    @dataclass(order=True)
    class PrioritizedState:
        """Dataclass to insert the RoomStates into the priority queue"""
        cost: int
        config: RoomState=field(compare=False)

    open_set = PriorityQueue()

    open_set.put(PrioritizedState(0, starting))

    closed_set = set()

    came_from = {} # map of pod config with the (pods, moved_pods)

    g_score = defaultdict(lambda: float('inf'))
    g_score[starting.pods] = 0

    def h_func(state: RoomState):
        # As the heuristic for the A* we will use the sum of distances
        # to the entrance of that amphipod room
        _cost = 0
        for i, pod_idx in enumerate(state.pods):
            type_ = get_pod_type(i)
            dest = destination_columns[type_]
            column = pod_idx % state.grid.cols
            if column != dest:
                dist =  mhd(state.grid.get_pos(pod_idx), (dest, 1))
                k = dist * move_cost[type_]
                _cost += k
        return _cost

    f_score = defaultdict(lambda: float('inf'))
    f_score[starting.pods] = h_func(starting)

    max_done = -1
    while not open_set.empty():
        item = open_set.get()
        current = item.config
        closed_set.add(current.pods)

        if current.is_finished():
            # if reached the best state, reconstruct the movements using
            # the came_from dictionary
            _cost = g_score[current.pods]
            pods = current.pods
            path = []
            while g_score[pods] != 0:
                path.append(pods)
                pods, _ = came_from[pods]

            current.pods = starting.pods
            current.moved_pods = []
            for pos in reversed(path):
                print(g_score[pos] - g_score[current.pods])
                current.pods = pos
                current.moved_pods = came_from[pos][1]
                print(current.render())
            return _cost

        # I render the first state which has more sorted to keep track of
        # the progress
        current_done = sum([1 for p in range(4*PODS_PER_TYPE) if current.is_done(p)])
        if current_done > max_done:
            print(current.render())
            max_done = current_done

        for _cost, new_state in get_moves(current):
            if new_state.pods in closed_set:
                continue

            tentative_g_score = g_score[current.pods] + _cost
            if tentative_g_score < g_score[new_state.pods]:
                # this is the better move
                came_from[new_state.pods] = (current.pods, new_state.moved_pods)
                g_score[new_state.pods] = tentative_g_score
                f_score[new_state.pods] = tentative_g_score + h_func(new_state)
                open_set.put(PrioritizedState(f_score[new_state.pods], new_state))

def make_part2(filename):
    extra = ["  #D#C#B#A#","  #D#B#A#C#"]
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        return __parse_input__(lines[:3] + extra + lines[3:])

if __name__ == '__main__':
    INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input23_test.txt"
    part1 = parse_input(INPUT_FILE)
    cost = find_best_path(part1)
    print(f"What is the least energy required to organize the amphipods? {cost}\n")

    part2 = make_part2(INPUT_FILE)
    cost = find_best_path(part2)
    print(f"What is the least energy required to organize the amphipods? {cost}")
