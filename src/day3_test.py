import unittest

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from day3 import *

class BinaryDiagnosticExampleTest(unittest.TestCase):
    """Unit tests for Day 3 using the problem example input."""
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


class BinaryDiagnosticMyInputTest(unittest.TestCase):
    """Unit tests for Day 3 using my puzzle input."""
    def setUp(self):
        self.bits, self.bit_length = read_input("input3.txt")

    def test_gamma(self):
        gamma = part1_calculate_gamma(self.bits, self.bit_length)
        self.assertEqual(bin(gamma), "0b10010010110")
        epsilon = part1_calculate_epsilon(gamma, self.bit_length)
        self.assertEqual(bin(epsilon), "0b101101101001")

    def test_answer1(self):
        gamma = part1_calculate_gamma(self.bits, self.bit_length)
        epsilon = part1_calculate_epsilon(gamma, self.bit_length)
        self.assertEqual(gamma*epsilon, 3429254)

    def test_oxigen(self):
        oxigen = part2_calculate_oxygen(self.bits, self.bit_length, True)
        self.assertEqual(bin(oxigen), "0b10110111111")

    def test_co2(self):
        co2 =   part2_calculate_oxygen(self.bits, self.bit_length, False)
        self.assertEqual(bin(co2), "0b111001011110")

    def test_answer2(self):
        oxigen = part2_calculate_oxygen(self.bits, self.bit_length, True)
        co2 = part2_calculate_oxygen(self.bits, self.bit_length, False)
        self.assertEqual(co2*oxigen, 5410338)

if __name__ == '__main__':
    unittest.main()
