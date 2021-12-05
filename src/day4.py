# https://adventofcode.com/2021/day/4

import sys
from copy import deepcopy

BINGO_SIZE = 5 # defined in problem

def create_board(lines):
    return [lines]

def parse_boards(lines):
    bingo_boards = []
    board_lines = []
    for l in lines:
        board_line = [int(n) for n in l.rstrip().split(" ",) if len(n) > 0]
        if (len(board_line) == 0):
            bingo_boards += [board_lines]
            board_lines = []
        else:
            board_lines += board_line
    if (len(board_lines) > 0):
        bingo_boards += [board_lines]
    return bingo_boards

def bingo_mark(number, bingo_board):
    if number in bingo_board:
        i = bingo_board.index(number)
        bingo_board[i] = -1
        return i
    return -1

def bingo_check(bingo_board):
    # check the if the amount of marked (-1) cells is equal to the bingo size for all rows and columns
    for i in range(BINGO_SIZE):
        if sum([1 if bingo_board[n*BINGO_SIZE + i]  == -1 else 0 for n in range(BINGO_SIZE)]) >= BINGO_SIZE:
            return True
        if sum([1 if bingo_board[i*BINGO_SIZE + n]  == -1 else 0 for n in range(BINGO_SIZE)]) >= BINGO_SIZE:
            return True
    return False

def bingo_check_fast(bingo_board, idx):
    # optimized version that only checks the row and colum of a given index
    row = int(idx / BINGO_SIZE)
    col = idx % BINGO_SIZE
    if sum([1 if bingo_board[n*BINGO_SIZE + col]  == -1 else 0 for n in range(BINGO_SIZE)]) >= BINGO_SIZE:
        return True
    if sum([1 if bingo_board[row*BINGO_SIZE + n]  == -1 else 0 for n in range(BINGO_SIZE)]) >= BINGO_SIZE:
        return True
    return False

def bingo_score(bingo_board):
    return sum([n for n in bingo_board if n != -1])
       
def part1_play_bingo(numbers, bingo_boards):
    for draw in numbers:
        for b in bingo_boards:
            bingo_mark(draw, b)
            if bingo_check(b):
                return draw * bingo_score(b)
    return 0
            
def part2_lose_bingo(numbers, bingo_boards):
    for draw in numbers:
        winning_boards = []
        for i,b in enumerate(bingo_boards):
            marked_idx = bingo_mark(draw, b)
            if marked_idx != -1: # only need to check when marking
                if bingo_check_fast(b, marked_idx):               
                    if (len(bingo_boards) == 1):
                        return draw * bingo_score(b)
                    else:
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

        score = part1_play_bingo(numbers, deepcopy(bingo_boards))
        print(f"What will your final score be if you choose that board? {score}")
        
        losing_score = part2_lose_bingo(numbers, deepcopy(bingo_boards))
        print(f"Once final board wins, what would its final score be? {losing_score}")


input_file = sys.argv[1] if len(sys.argv) > 1 else "input4.txt"
main("input4_test.txt")
main(input_file)
