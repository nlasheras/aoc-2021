# https://adventofcode.com/2021/day/23

from utils import Grid, TermColors
from dataclasses import dataclass, field
from typing import Tuple, List
from copy import copy
from functools import cache

destination_columns = { 'A': 3, 'B': 5, 'C': 7, 'D': 9 }
move_cost = { 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }

## this will be updated on parse_input
pods_per_type = 2
destination_indexes = {} # dict 

def char_from_type(type:int) -> str:
    return chr(65 + type)

def get_pod_type(idx: int) -> str:
    return char_from_type(idx // pods_per_type)

@dataclass(order=False)
class RoomState:
    grid: Grid
    pods: Tuple[int] # pos of each amphipod
    moved_pods: List[int] # idx of moving pods

    def __copy__(self) -> 'RoomState':
        return RoomState(self.grid, copy(self.pods), copy(self.moved_pods))

    # I'm using @cache for the get_path function I want
    def __hash__(self) -> int:
        return self.grid.rows * self.grid.cols
    def __eq__(self, o) -> bool:
        return self.__hash__() == o.__hash__()

    def is_finished(self):
        for type in range(4):
            pods_in_room = sorted(self.pods[pods_per_type*type:pods_per_type*(type+1)])
            correct_pods = destination_indexes[char_from_type(type)]
            if pods_in_room != correct_pods:
                return False
        return True

    def get_pod_at_pos(self, pos : Tuple[int]):
        idx = self.grid.get_idx(pos)
        return self.get_pod_at_grid(idx)
    
    def get_pod_at_grid(self, idx: int):
        if idx in self.pods:
            return self.pods.index(idx)
        return None

    def render(self):
        render = ""
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                pod = self.get_pod_at_pos((col, row))
                if pod is not None:
                    type = pod // pods_per_type

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
                    render += char_from_type(type)
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
        dx = dcol - fcol
        dy = drow - frow

        def sign(a):
            return 1 if a >= 0 else - 1

        path = []
        if frow > 1:
            for i in range(1, abs(dy)+1):
                path.append((fcol, frow+i*sign(dy)))
            for i in range(1, abs(dx)+1):
                path.append((fcol+i*sign(dx), drow))
        else:
            for i in range(1, abs(dx)+1):
                path.append((fcol+i*sign(dx), frow))
            for i in range(1, abs(dy)+1):
                path.append((dcol, frow+i*sign(dy)))

        return [self.grid.get_idx(p) for p in path]

    @cache
    def get_hallway_moves(self, from_idx):
        """Returns the indices of the valid hallway postions for a move of
        an amphipod in a given position."""
        col, row = self.grid.get_pos(from_idx)
        assert(row == 1)
        if row == 1:
            moves = []
            
            if col > 2: moves += [(col-2, 1)]
            elif col > 1: moves += [(col-1, 1)]

            grid_columns = self.grid.cols
            if col < grid_columns - 3: moves += [(col+2, 1)]
            elif col < grid_columns - 2: moves += [(col+1, 1)]

            return [self.grid.get_idx(p) for p in moves \
                if p[0] not in destination_columns.values()]
        return []

    def get_top_pod_in_rooms(self):
        ret = []
        for room in ('A', 'B', 'C', 'D'):
            for grid_idx in destination_indexes[room]:
                if grid_idx in self.pods:
                    i = self.pods.index(grid_idx)
                    if not self.is_done(i):
                        ret += [i]
                        break
        return ret
    
    def get_empty_spot_in_room(self, room):
        if room in destination_indexes:
            indexes = destination_indexes[room]
            for grid_idx in reversed(indexes):
                if grid_idx in self.pods:
                    if not self.is_done(self.pods.index(grid_idx)):
                        return None # cannot go back to the room yet
                else:
                    return grid_idx
        return None

    def is_done(self, idx):
        grid_idx = self.pods[idx]
        col, row = self.grid.get_pos(grid_idx)
        type = self.pods.index(grid_idx) // pods_per_type
        if col == destination_columns[chr(65 + type)]:
            if row >= 1: 
                for i in range(row+1, self.grid.rows - 1):
                    other = self.get_pod_at_pos((col, i))
                    if other is None:
                        return False
                    else:
                        other_type = other // pods_per_type
                        if type != other_type:
                            return False
                return True
        return False

def parse_input(filename):
    with open(filename, "r") as file:
        return __parse_input__(file.readlines())

def __parse_input__(lines):
    # parse file into a grid
    g = Grid()
    for i,line in enumerate(lines):
        row = [c for c in line.rstrip()]
        if i == 0: 
            g.cols = len(row)
        else: 
            row += [' '] * (g.cols - len(row))
        g.cells += row
    g.rows = (len(g.cells) // g.cols)

    # get the pods into a List of tuples (type, x, y)
    pods = []
    for row in range(g.rows):
        for col in range(g.cols):
            idx = g.get_idx((col, row))
            value = g.cells[idx]
            if value == 'A' or value == 'B' or value == 'C' or value == 'D':
                g.cells[idx] = '.'
                pods.append((value, col, row))

    pods_idx = []
    for c in range(ord('A'), ord('D')+1):
        for p in pods:
            if p[0] == chr(c):
                pods_idx.append(g.get_idx((p[1], p[2])))

    global pods_per_type
    pods_per_type = len(pods_idx) // 4
    assert(len(pods_idx) % pods_per_type == 0)

    global destination_indexes
    destination_indexes = {}
    for type in range(4):
        dest = []
        c = char_from_type(type)
        for i in range(2, 2+pods_per_type):
            pos = (destination_columns[c], i)
            dest += [g.get_idx(pos)]
        destination_indexes[c] = dest

    return RoomState(g, tuple(pods_idx), [])

def mhd(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
def is_path_free(current: RoomState, from_idx, to_idx):
    for idx in current.get_path(from_idx, to_idx):
        if idx in current.pods:
            return False
    return True

def get_moves(current: RoomState):
    moves = []
            
    for p in reversed(current.moved_pods):
        if current.is_done(p):
            continue
        if p == current.moved_pods[-1]:
            # do moves por current moving pod
            p_pos = current.pods[p]
            moves += [(p, idx) for idx in current.get_hallway_moves(p_pos)]

        type = get_pod_type(p)
        empty_spot_idx = current.get_empty_spot_in_room(type)
        if empty_spot_idx:
            moves += [(p, empty_spot_idx)]

    for p in current.get_top_pod_in_rooms():
        assert(not p in current.moved_pods)
        p_pos = current.pods[p]
        col, _ = current.grid.get_pos(p_pos)
        out_pos = [(col-1, 1), (col+1, 1)]
        for pos in out_pos:
            out_idx = current.grid.get_idx(pos)
            moves += [(p, out_idx)]

    # translate moves tuples (pod, grid_idx) into Move
    ret = []
    for pod, dest_idx in moves:
        from_idx = current.pods[pod]
        if not is_path_free(current, from_idx, dest_idx):
            continue

        type = get_pod_type(pod)
        config = copy(current)
        # replace the index of config.pod[pod]
        config.pods = tuple(dest_idx if p == pod else idx for p, idx in enumerate(current.pods)) 
        
        def dist(idx1, idx2):
            return mhd(current.grid.get_pos(idx1), current.grid.get_pos(idx2))

        cost = move_cost[type] * dist(from_idx, dest_idx)

        if not pod in config.moved_pods:
            config.moved_pods.append(pod)
        elif pod != config.moved_pods[-1]:
            # whenever a amphipod moves, it moves to the end of moved_pod list
            config.moved_pods.remove(pod)
            config.moved_pods.append(pod)

        ret.append((cost, config))

    return ret

from queue import PriorityQueue
from collections import defaultdict

@dataclass(order=True)
class PrioritizedState:
    cost: int
    config: RoomState=field(compare=False)

def find_best_path(starting):
    open_set = PriorityQueue()
    
    open_set.put(PrioritizedState(0, starting))

    closed_set = set()

    came_from = {} # map of pod config with the (pods, moved_pods)
    
    gScore = defaultdict(lambda: float('inf'))
    gScore[starting.pods] = 0

    def h_func(state: RoomState):
        # As the heuristic for the A* we will use the sum of distances
        # to the entrance of that amphipod room
        sum = 0
        for i, pod_idx in enumerate(state.pods):
            type = get_pod_type(i)
            dest = destination_columns[type]
            column = pod_idx % state.grid.cols
            if column != dest:
                dist =  mhd(state.grid.get_pos(pod_idx), (dest, 1)) 
                k = dist * move_cost[type]
                sum += k
        return sum
 
    fScore = defaultdict(lambda: float('inf'))
    fScore[starting.pods] = h_func(starting)

    max_done = -1
    while not open_set.empty():
        item = open_set.get()
        current = item.config
        closed_set.add(current.pods)

        if current.is_finished():
            # if reached the best state, reconstruct the movements using
            # the came_from dictionary
            cost = gScore[current.pods]
            pods = current.pods
            path = []
            while (gScore[pods] != 0):
                path.append(pods)
                pods, _ = came_from[pods]

            current.pods = starting.pods
            current.moved_pods = []
            for p in reversed(path):
                print(gScore[p] - gScore[current.pods])
                current.pods = p
                current.moved_pods = came_from[p][1]
                print(current.render())
            return cost

        # I render the first state which has more sorted to keep track of 
        # the progress
        current_done = sum([1 for p in range(4*pods_per_type) if current.is_done(p)])
        if current_done > max_done:
            print(current.render())
            max_done = current_done

        for cost, new_state in get_moves(current):
            if new_state.pods in closed_set:
                continue

            tentative_gScore = gScore[current.pods] + cost
            if tentative_gScore < gScore[new_state.pods]:
                # this is the better move
                came_from[new_state.pods] = (current.pods, new_state.moved_pods)
                gScore[new_state.pods] = tentative_gScore
                fScore[new_state.pods] = tentative_gScore + h_func(new_state)
                open_set.put(PrioritizedState(fScore[new_state.pods], new_state))
    
def make_part2(filename):
    extra = ["  #D#C#B#A#","  #D#B#A#C#"]
    with open(filename, "r") as file:
        lines = file.readlines()
        return __parse_input__(lines[:3] + extra + lines[3:])

import sys
if __name__ == '__main__':
    input = sys.argv[1] if len(sys.argv) > 1 else "input23_test.txt" 
    part1 = parse_input(input)
    cost = find_best_path(part1)
    print(f"What is the least energy required to organize the amphipods? {cost}\n")

    part2 = make_part2(input)
    cost = find_best_path(part2)
    print(f"What is the least energy required to organize the amphipods? {cost}")

