#https://adventofcode.com/2021/day/3

def part1_calculate_gamma(inputs, bit_length):
    gamma_sum = [0] * bit_length
    for number in inputs:
        for i in range(bit_length):
            gamma_sum[i] += 1 if number & (1 << (bit_length - i - 1)) else 0

    n = len(inputs)
    gamma = "".join(['1' if sum > n/2 else '0' for sum in gamma_sum])
    return gamma

def match_gamma(value, gamma, gamma_mask):
    return not (value & gamma_mask) ^ (gamma & gamma_mask)

def part2_calculate_oxygen(inputs, bit_length, bit):
    inverse_bit = 0 if bit == 1 else 1
    gamma = 0
    gamma_mask = 0
    for i in range(bit_length):
        matching_lines = [n for n in inputs if match_gamma(n, gamma, gamma_mask)]
        if (len(matching_lines) == 1): 
            return matching_lines[0]
        elif (len(matching_lines) == 2):
             return matching_lines[0] if matching_lines[0] & gamma_mask == bit else matching_lines[1]

        gamma_sum = 0
        for number in matching_lines:
            gamma_sum += 1 if number & (1 << (bit_length - i - 1)) else 0

        gamma_bit = bit if gamma_sum >= int((len(matching_lines)+1)/2) else inverse_bit
        gamma = gamma | (gamma_bit << (bit_length - i - 1))
        gamma_mask = gamma_mask | (1 << (bit_length - i - 1))

    
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

    gamma_str = part1_calculate_gamma(bits, bit_length)
    # since epsilon is using the least common bits you can get it negating gamma
    epsilon_str = "".join(['1' if c == '0' else '0' for c in gamma_str])

    epsilon = int(epsilon_str, 2)
    gamma = int(gamma_str, 2)

    print("gamma rate: {0} ({1})".format(gamma_str, gamma))
    print("epsilon rate: {0} ({1})".format(epsilon_str, epsilon))
    print("What is the power consumption of the submarine?: {0}".format(gamma*epsilon))

    oxigen = part2_calculate_oxygen(bits, bit_length, 1)
    co2 = part2_calculate_oxygen(bits, bit_length, 0)

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

        def test_gamma_str(self):
            gamma_str = part1_calculate_gamma(self.bits, self.bit_length)
            self.assertEqual(gamma_str, "10110")

        def test_oxigen(self):
            oxigen = part2_calculate_oxygen(self.bits, self.bit_length, 1)
            self.assertEqual(bin(oxigen), "0b10111")

        def test_co2(self):
            co2 =   part2_calculate_oxygen(self.bits, self.bit_length, 0)
            self.assertEqual(bin(co2), "0b1010")

    unittest.main()


if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input3.txt"
    # expected solutions 3429254, 5410338
    main(input_file)