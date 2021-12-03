#https://adventofcode.com/2021/day/3

import sys

input_file = sys.argv[1]

def part1_calculate_gamma(lines):
    gamma_sum = [0] * len(lines[0].rstrip())
    for l in lines:
        for i, char in enumerate(l.rstrip()):
            gamma_sum[i] += int(char)

    n = len(lines)
    gamma = ""
    for sum in gamma_sum:
        if sum >= n/2: gamma += "1"
        else: gamma += "0"

    return gamma

def match_gamma(str, gamma, chars):
    for i in range(chars):
        if gamma[i] != str[i]: return False
    return True

def part2_calculate_oxygen(lines, bit = "1"):
    inverse_bit = "0" if bit == "1" else "1"
    bit_length = len(lines[0].rstrip())
    gamma_sum = [0] * bit_length
    gamma = ""
    for i in range(bit_length):
        matching_lines = [l for l in lines if match_gamma(l, gamma, i)]
        if (len(matching_lines) == 1): 
            return matching_lines[0]
        elif (len(matching_lines) == 2):
             return matching_lines[0] if matching_lines[0][i] == bit else matching_lines[1]
        for l in matching_lines:
            gamma_sum[i] += int(l[i])
        gamma += bit if gamma_sum[i] >= int((len(matching_lines)+1)/2) else inverse_bit
    
    # not defined in the problem
    return gamma

with open(input_file, newline='',encoding='utf-8') as file:

    lines = file.readlines()

    epsilon_str = part1_calculate_gamma(lines)
    # since gamma is using the least common bits you can get it negating epsilon
    gamma_str = "".join(['1' if c == '0' else '0' for c in epsilon_str])

    epsilon = int(epsilon_str, 2)
    gamma = int(gamma_str, 2)

    print("What is the power consumption of the submarine?: {0}".format(gamma*epsilon))

    oxigen_str = part2_calculate_oxygen(lines, "1")
    co2_str = part2_calculate_oxygen(lines, "0")

    oxigen = int(oxigen_str, 2)
    co2 = int(co2_str, 2)

    print("What is the life support rating of the submarine?: {0}".format(oxigen*co2))

