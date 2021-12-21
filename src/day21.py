# https://adventofcode.com/2021/day/21

from copy import copy

class Game:
    def __init__(self, spaces, scores, current_player = 0):
        self.pawns = spaces
        self.scores = scores
        self.current_player = current_player

    def play_once(self, rolls):
        TRACK_LENGTH = 10
        self.pawns[self.current_player] = (self.pawns[self.current_player] + sum(rolls)) % TRACK_LENGTH
        self.scores[self.current_player] += self.pawns[self.current_player] + 1
        self.current_player = (self.current_player + 1) % 2

    def __hash__(self) -> int:
        return hash(tuple(self.pawns + self.scores + [self.current_player]))
    
    def __eq__(self, __o: object) -> bool:
        return self.__hash__() == __o.__hash__()
    
    def __repr__(self):
        return f"pawns {self.pawns} score {self.scores[0]}-{self.scores[1]} next: {self.current_player}"
    
    def __copy__(self):
        return Game(copy(self.pawns), copy(self.scores), self.current_player)

class DeterministicDice:
    def __init__(self):
        self.next = 1
        self.rolls = 0

    def roll(self):
        result = self.next
        self.rolls += 1
        self.next += 1
        if self.next > 100:
            self.next = 1
        return result

def part1_play_deterministic(pawn1, pawn2):
    d = DeterministicDice()
    g = Game([pawn1-1, pawn2-1], [0, 0], 0)
    while max(g.scores) < 1000:
        rolls = [d.roll() for i in range(3)]
        g.play_once(rolls)

    part1 = min(g.scores) * d.rolls
    print(f"What do you get if you multiply the score of the losing player by the number of times the die was rolled during the game? {part1}")

from functools import cache
from itertools import product

@cache
def count_wins(g):
    assert(max(g.scores) < 21)

    wins = (0, 0)
    for roll in product([1,2,3], repeat=3):
        qg = copy(g)
        qg.play_once(roll)
        if max(qg.scores) >= 21:
            qwins = (1, 0) if qg.scores.index(max(qg.scores)) == 0 else (0, 1)
        else:
            qwins = count_wins(qg)
        wins = (wins[0] + qwins[0], wins[1] + qwins[1])
    
    return wins

def part2_play_dirac(pawn1, pawn2):
    g = Game([pawn1-1, pawn2-1], [0, 0], 0)
    wins = count_wins(g)
    print(f"Find the player that wins in more universes; in how many universes does that player win? {max(wins)}")   

if __name__ == '__main__':
    part1_play_deterministic(4,8)
    part1_play_deterministic(4,10)
 
    print("\n", end='')  
    part2_play_dirac(4,8)
    part2_play_dirac(4,10)