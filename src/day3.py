#https://adventofcode.com/2021/day/3

import math
from copy import deepcopy

def part1_calculate_gamma(inputs, bit_length):
    gamma_sum = [0] * bit_length
    for number in inputs:
        for i in range(bit_length):
            gamma_sum[i] += 1 if number & (1 << (bit_length - i - 1)) else 0

    n = len(inputs)
    gamma = 0
    for i, sum in filter(lambda x: x[1] > int(n/2), enumerate(gamma_sum)):
        gamma += 1 << (bit_length - i - 1)

    return gamma

def part1_calculate_epsilon(gamma, bit_length):
    # since epsilon is using the least common bits you can get it negating gamma
    bit_mask = int("1" * bit_length, 2)
    return bit_mask & ~gamma

def match_gamma(value, gamma, gamma_mask):
    return not (value & gamma_mask) ^ (gamma & gamma_mask)

def part2_calculate_oxygen(inputs, bit_length, most_common):
    gamma = 0
    gamma_mask = 0
    for i in range(bit_length-1, -1, -1):
        if gamma_mask != 0:
            matching_lines = [n for n in matching_lines if match_gamma(n, gamma, gamma_mask)]
        else:
            matching_lines = inputs # saving one listcomp
        
        n = len(matching_lines)
        bit_mask = 1 << i
        count_ones = sum([1 if n & bit_mask else 0 for n in matching_lines])
        count_zeros = n - count_ones

        if most_common:
            gamma_bit = 1 if count_ones >= count_zeros else 0
        else:
            gamma_bit = 0 if count_zeros <= count_ones else 1 

        if (n == 1): # stop when only 1 number finishes
            return matching_lines[0] 
        elif (n == 2): 
            return matching_lines[0] if matching_lines[0] & gamma_mask == gamma_bit else matching_lines[1]

        gamma = gamma | (gamma_bit << i)
        gamma_mask = gamma_mask | bit_mask
    
    # not defined in the problem
    return gamma


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

    print("gamma rate: {0} ({1})".format(bin(gamma), gamma))
    print("epsilon rate: {0} ({1})".format(bin(epsilon), epsilon))
    print("What is the power consumption of the submarine?: {0}".format(gamma*epsilon))

    oxigen = part2_calculate_oxygen(bits, bit_length, True)
    co2 = part2_calculate_oxygen(bits, bit_length, False)

    print("oxigen generator rating: {0} ({1})".format(bin(oxigen), oxigen))
    print("CO2 scrubber rating: {0} ({1})".format(bin(co2), co2))
    print("What is the life support rating of the submarine?: {0}".format(oxigen*co2))


import sys

if "unittest" in sys.argv:
    sys.argv.remove("unittest")

    import unittest
    class BinaryDiagnosticTest(unittest.TestCase):
        def setUp(self):
            self.bits, self.bit_length = read_input("input3_test.txt")

        def test_gamma(self):
            gamma = part1_calculate_gamma(self.bits, self.bit_length)
            self.assertEqual(bin(gamma), "0b10110")
            epsilon = part1_calculate_epsilon(gamma, self.bit_length)
            self.assertEqual(bin(epsilon), "0b1001")

        def test_oxigen(self):
            oxigen = part2_calculate_oxygen(self.bits, self.bit_length, True)
            self.assertEqual(bin(oxigen), "0b10111")

        def test_co2(self):
            co2 =   part2_calculate_oxygen(self.bits, self.bit_length, False)
            self.assertEqual(bin(co2), "0b1010")

    unittest.main()


if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input3.txt"
    # expected solutions 3429254, 5410338
    main(input_file)