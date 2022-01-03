""" https://adventofcode.com/2021/day/10 """

from functools import reduce

def read_input(filename):
    with open(filename, "r", encoding='utf-8') as file:
        return [l.rstrip() for l in file.readlines()]

opening_map = { ")": "(", "]": "[", "}": "{", ">": "<" }
closing_map = {v: k for k,v in opening_map.items()}

def parse(line):
    points = { ")": 3, "]": 57, "}": 1197, ">": 25137 }
    error_score = 0
    stack = []
    for _c in line:
        if _c in opening_map: # it's a closing character
            expecting = opening_map[_c]
            top = stack[-1]
            if expecting == top:
                stack.pop()
            else:
                return points[_c], stack
        else:
            stack.append(_c)
    return error_score, stack

def part1_syntax_error(lines):
    tuples = [parse(l) for l in lines]
    print(f"What is the total syntax error score for those errors? {sum([t[0] for t in tuples])}")

def part2_autocompletion(lines):
    valid_lines = filter(lambda t: t[0] == 0, [parse(l) for l in lines]) # valid lines have score 0

    def score(stack):
        autocomplete_points = { ")": 1, "]": 2, "}": 3, ">": 4}
        completion_string = [closing_map[c] for c in reversed(stack)]
        return reduce(lambda acc, x: acc*5 + x, [autocomplete_points[c] for c in completion_string], 0)

    scores = [score(t[1]) for t in valid_lines]
    middle_score = sorted(scores)[len(scores)//2]
    print(f"What is the middle score? {middle_score}")

if __name__ == '__main__':
    input_lines = read_input("input10_test.txt")
    part1_syntax_error(input_lines)
    part2_autocompletion(input_lines)

    input_lines = read_input("input10.txt")
    part1_syntax_error(input_lines)
    part2_autocompletion(input_lines)
