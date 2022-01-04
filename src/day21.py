""" https://adventofcode.com/2021/day/21 """

from copy import copy
from functools import cache
from itertools import product
from collections import defaultdict

class Game:
    """Implement the dirac dice game simulation"""
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
    """Deterministic dice for part 1"""
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
    """Simple implementation of part 1 just simulating it with Game"""
    dice = DeterministicDice()
    game = Game([pawn1-1, pawn2-1], [0, 0], 0)
    while max(game.scores) < 1000:
        rolls = [dice.roll() for _ in range(3)]
        game.play_once(rolls)

    part1 = min(game.scores) * dice.rolls
    print(f"What do you get if you multiply the score of the losing player by the number of times the die was rolled during the game? {part1}")

# instead of using the full product, we can cache the sum(rolls) since it doesn't
# matter the order of the individual dice rolls just the amount of steps the pawn
# advances
def __cache_rolls__():
    result = defaultdict(int)
    for roll in product([1,2,3], repeat=3):
        result[sum(roll)] += 1
    return result.items()

rolls_3d3 = __cache_rolls__()

@cache
def count_wins(game):
    assert max(game.scores) < 21

    wins = (0, 0)
    for roll, frequency in rolls_3d3:
        quantum_game = copy(game)
        quantum_game.play_once([roll])
        if max(quantum_game.scores) >= 21:
            quantum_wins = (1, 0) if quantum_game.scores.index(max(quantum_game.scores)) == 0 else (0, 1)
        else:
            quantum_wins = count_wins(quantum_game)
        wins = (wins[0] + frequency*quantum_wins[0], wins[1] + frequency*quantum_wins[1])

    return wins

def part2_play_dirac(pawn1, pawn2):
    start = Game([pawn1-1, pawn2-1], [0, 0], 0)
    wins = count_wins(start)
    print(f"Find the player that wins in more universes; in how many universes does that player win? {max(wins)}")

if __name__ == '__main__':
    part1_play_deterministic(4,8)
    part1_play_deterministic(4,10)

    print("\n", end='')
    part2_play_dirac(4,8)
    part2_play_dirac(4,10)
