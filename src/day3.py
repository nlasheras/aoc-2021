""" https://adventofcode.com/2021/day/3 """

import sys

def bit_iterator(bit_length):
    """Get an iterator for the bits in left to right order"""
    return range(bit_length-1, -1, -1)

def part1_calculate_gamma(inputs, bit_length):
    """Gamma rate is equal to the most common bit for each position"""
    #count how many ones are in each position for the input numbers
    count_ones = [0] * bit_length
    for number in inputs:
        for i in bit_iterator(bit_length):
            count_ones[i] += 1 if number & (1 << i) else 0

    # set to 1 the bits where there is more ones than half of the inputs
    input_amount = len(inputs)
    gamma_bits = list(map(lambda x: 1 if x > int(input_amount/2) else 0, count_ones))
    gamma = 0
    for bit, value in enumerate(gamma_bits):
        gamma |= value << bit

    return gamma

def part1_calculate_epsilon(gamma, bit_length):
    """Epsilon rate is equal to the least common bit for each position, it
    can be calculated by just negating the most common bits (gamma rate)"""
    bit_mask = int("1" * bit_length, 2)
    return bit_mask & ~gamma

def match_gamma(value, gamma, gamma_mask):
    """Do a bitwise check of value with gamma using only the bits from gamma_mask"""
    return not (value & gamma_mask) ^ (gamma & gamma_mask)

def part2_calculate_oxygen(inputs, bit_length, most_common):
    """To calculate oxygen generator rating and CO2 scrubber rating we are looking
    for a number that matches the a criteria bit by bit until we get only one."""
    gamma = 0
    gamma_mask = 0 # we will build a mask of the bits that the number must match
    for i in bit_iterator(bit_length):
        if gamma_mask != 0:
            matching_lines = [n for n in matching_lines if match_gamma(n, gamma, gamma_mask)]
        else:
            matching_lines = inputs # saving one listcomp since with mask 0 all match

        line_amount = len(matching_lines)
        bit_mask = 1 << i
        count_ones = sum([1 if n & bit_mask else 0 for n in matching_lines])
        count_zeros = line_amount - count_ones

        if most_common:
            gamma_bit = 1 if count_ones >= count_zeros else 0
        else:
            gamma_bit = 0 if count_zeros <= count_ones else 1

        if line_amount == 1: # stop when only 1 number finishes
            return matching_lines[0]
        if line_amount == 2:
            # equally common rule applied to decide between two numbers
            if matching_lines[0] & gamma_mask == gamma_bit:
                return matching_lines[0]
            return matching_lines[1]

        gamma |= gamma_bit << i
        gamma_mask |= bit_mask

    # not defined in the problem
    assert False
    return -1

def read_input(input_file):
    with open(input_file, newline='',encoding='utf-8') as file:
        lines = file.readlines()

        bit_length = len(lines[0].rstrip())
        bits = [int(l, 2) for l in lines]
        return bits, bit_length
    return [], 0

def main(input_file):
    bits, bit_length = read_input(input_file)

    gamma = part1_calculate_gamma(bits, bit_length)
    epsilon = part1_calculate_epsilon(gamma, bit_length)

    print(f"gamma rate: {bin(gamma)} ({gamma})")
    print(f"epsilon rate: {bin(epsilon)} ({epsilon})")
    print(f"What is the power consumption of the submarine?: {gamma*epsilon}")

    oxigen = part2_calculate_oxygen(bits, bit_length, True)
    co2 = part2_calculate_oxygen(bits, bit_length, False)

    print(f"oxigen generator rating: {bin(oxigen)} ({oxigen})")
    print(f"CO2 scrubber rating: {bin(co2)} ({co2})")
    print(f"What is the life support rating of the submarine?: {oxigen*co2}")

if __name__ == '__main__':
    INPUT_FILE = sys.argv[1] if len(sys.argv) > 1 else "input3.txt"
    main(INPUT_FILE)
