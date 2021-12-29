""" https://adventofcode.com/2021/day/4 """

import sys
from copy import copy

BINGO_SIZE = 5 # defined in problem

def create_board(lines):
    return [lines]

def parse_boards(lines):
    bingo_boards = []
    board_lines = []
    for _l in lines:
        board_line = [int(n) for n in _l.rstrip().split(" ",) if len(n) > 0]
        if len(board_line) == 0:
            bingo_boards += [board_lines]
            board_lines = []
        else:
            board_lines += board_line
    if len(board_lines) > 0:
        bingo_boards += [board_lines]
    return bingo_boards

def bingo_mark(number, bingo_board):
    if number in bingo_board:
        i = bingo_board.index(number)
        bingo_board[i] = -1
        return i
    return -1

def __bingo_check_col_row__(bingo_board, col, row):
    if all(map(lambda x, col=row: bingo_board[x*BINGO_SIZE + col] == -1, range(BINGO_SIZE))):
        return True
    if all(map(lambda x, row=col: bingo_board[row*BINGO_SIZE + x] == -1, range(BINGO_SIZE))):
        return True
    return False

def bingo_check(bingo_board):
    """ Check the if the amount of marked (-1) cells is equal to the bingo size
    for all rows and columns"""
    for i in range(BINGO_SIZE):
        if __bingo_check_col_row__(bingo_board, i, i):
            return True
    return False

def bingo_check_fast(bingo_board, idx):
    """Faster version of bingo_check that only looks at the row and colum of a given index"""
    row = int(idx / BINGO_SIZE)
    col = idx % BINGO_SIZE
    return __bingo_check_col_row__(bingo_board, col, row)

def bingo_score(bingo_board):
    return sum([n for n in bingo_board if n != -1])

def part1_play_bingo(numbers, bingo_boards):
    for draw in numbers:
        for board in bingo_boards:
            bingo_mark(draw, board)
            if bingo_check(board):
                return draw * bingo_score(board)
    return 0

def part2_lose_bingo(numbers, bingo_boards):
    for draw in numbers:
        winning_boards = []
        for i, board in enumerate(bingo_boards):
            marked_idx = bingo_mark(draw, board)
            if marked_idx != -1: # only need to check when marking
                if bingo_check_fast(board, marked_idx):
                    if len(bingo_boards) == 1:
                        return draw * bingo_score(board)
                    winning_boards += [i]

        winning_boards.reverse()
        for idx in winning_boards:
            bingo_boards = bingo_boards[:idx] + bingo_boards[idx+1:]
    return 0

def main(input_file):
    with open(input_file, newline='',encoding='utf-8') as file:
        lines = file.readlines()

        numbers = [int(n) for n in lines[0].rstrip().split(",")]

        bingo_boards = parse_boards(lines[2:])

        score = part1_play_bingo(numbers, copy(bingo_boards))
        print(f"What will your final score be if you choose that board? {score}")

        losing_score = part2_lose_bingo(numbers, copy(bingo_boards))
        print(f"Once final board wins, what would its final score be? {losing_score}")


if __name__ == '__main__':
    INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input4.txt"
    main(INPUT_FILE)
