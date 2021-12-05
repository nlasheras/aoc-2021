import unittest
from day3 import *

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

if __name__ == '__main__':
    unittest.main()
