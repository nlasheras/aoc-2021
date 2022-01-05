# https://adventofcode.com/2021/day/8

import itertools

# pylint: disable=invalid-name

def parse_entries(filename):
    with open(filename, newline='',encoding='utf-8') as file:
        entries = []
        lines = file.readlines()
        for line in lines:
            split = line.split(" | ")
            entries += [(split[0].rstrip().split(" "), split[1].rstrip().split(" "))]
        return entries

def part1(filename):
    entries = parse_entries(filename)
    output_values = [e[1] for e in entries]

    def test_1478(v):
        return len(v) == 2 or len(v) == 3 or len(v) == 4 or len(v) == 7

    count = sum(map(lambda x: sum([1 for s in x if test_1478(s)]), output_values))

    print(f"In the output values, how many times do digits 1, 4, 7, or 8 appear? {count}")

# I will assign each letter a,g to bits 0->7 to use bitwise operations to check masks
def mask(pattern):
    bits = 0
    for c in pattern:
        bits |= 1 << ord(c) - ord('a')
    return bits

def deduct_pattern(inputs):
    deducted_numbers = [""] * 10
    deducted_masks = [0] * 10

    bit_mask = 0x7f

    def assign(s, n):
        deducted_numbers[n] = s
        deducted_masks[n] = mask(deducted_numbers[n])

    def find_and_assign(n, inputs, test):
        passed = [i for i in inputs if test(i)]
        if len(passed) > 1:
            count_different = sum([1 for s in passed[1:] if mask(s) != mask(passed[0])])
            if count_different:
                print(f"Multiple patterns found for {n}: {passed}")
        if len(passed) > 0:
            assign(passed[0], n)
        else:
            print(f"{n} not found!")

    def match(a, b):
        return (a^b) & b == 0
    def flip(m):
        return ~m & bit_mask

    find_and_assign(1, inputs, lambda s: len(s) == 2)
    find_and_assign(8, inputs, lambda s: len(s) == 7)
    find_and_assign(7, inputs, lambda s: len(s) == 3)
    find_and_assign(4, inputs, lambda s: len(s) == 4)

    len6 = [s for s in inputs if len(s) == 6]
    seg_a = deducted_masks[7] & flip(deducted_masks[1])
    t9 = deducted_masks[4] | seg_a
    find_and_assign(9, len6, lambda s: match(mask(s), t9))

    t6 = deducted_masks[9] & flip(deducted_masks[7])
    find_and_assign(6, len6, lambda s: match(mask(s), t6) and not match(mask(s), t9))

    find_and_assign(0, len6, \
        lambda s: not (match(mask(s), deducted_masks[6]) or match(mask(s), deducted_masks[9])))

    len5 = [s for s in inputs if len(s) == 5]
    find_and_assign(2, len5, lambda s: match(mask(s), flip(deducted_masks[9])))

    find_and_assign(5, len5, lambda s: mask(s) | deducted_masks[1] == deducted_masks[9])

    find_and_assign(3, len5, lambda s: mask(s) & deducted_masks[7] == deducted_masks[7])

    class SignalPattern:
        """Helper class that contains the deducted masks and can be used to decode entries"""
        def __init__(self, masks):
            self.number_masks = masks

        def decode(self, entry):
            digits = [self.number_masks.index(mask(pattern)) for pattern in entry]
            return sum(map(lambda x: pow(10, x[0])*x[1], enumerate(reversed(digits))))

    return SignalPattern(deducted_masks)

def part2(filename):
    entries = parse_entries(filename)
    output_sum = 0
    for e in entries:
        d = deduct_pattern(e[0] + e[1])
        output = d.decode(e[1])
        #print(f"{e[1]} = {output}")
        output_sum += output

    print(f"What do you get if you add up all of the output values? {output_sum}")

# pylint: disable=multiple-statements
def deduct_bf(numbers):
    inputs = ["".join(sorted(s)) for s in numbers]

    def not_found(pattern):
        sp = "".join(sorted(pattern))
        return not sp in inputs

    for a,b,c,d,e,f,g in itertools.permutations('abcdefg'):
        if not_found(a+b): continue # 1
        if not_found(a+b+d): continue # 7
        if not_found(a+b+e+f): continue # 4
        if not_found(a+b+c+d+e+f+g): continue # 8

        if not_found(c+a+g+e+d+b): continue # 0
        if not_found(g+c+d+f+a): continue # 2
        if not_found(f+b+c+a+d): continue # 3
        if not_found(c+d+f+b+e): continue # 5
        if not_found(c+d+f+g+e+b): continue # 6
        if not_found(c+e+f+a+b+d): continue # 9

        class SignalPattern:
            """Use same API than other version of deduct_pattern"""
            def __init__(self, a,b,c,d,e,f,g): # pylint: disable=too-many-arguments
                self.dict = {}

                def __add_key__(pattern, number):
                    self.dict["".join(sorted(pattern))] = number

                __add_key__(a+b, 1)
                __add_key__(a+b+d, 7)
                __add_key__(a+b+e+f, 4)
                __add_key__(a+b+c+d+e+f+g, 8)

                __add_key__(c+a+g+e+d+b, 0)
                __add_key__(g+c+d+f+a, 2)
                __add_key__(f+b+c+a+d, 3)
                __add_key__(c+d+f+b+e, 5)
                __add_key__(c+d+f+g+e+b, 6)
                __add_key__(c+e+f+a+b+d, 9)

            def decode(self, entry):
                digits = [self.dict["".join(sorted(s))] for s in entry]
                return sum(map(lambda x: pow(10, x[0])*x[1], enumerate(reversed(digits))))

        return SignalPattern(a,b,c,d,e,f,g)


def part2_bf(filename):
    entries = parse_entries(filename)
    ouput_sum = 0
    for e in entries:
        d = deduct_bf(e[0] + e[1])
        output = d.decode(e[1])
        ouput_sum += output

    print(f"What do you get if you add up all of the output values? {ouput_sum}")

if __name__ == '__main__':
    part1("input8_test.txt")
    part1("input8.txt")
    part2("input8_test.txt")
    part2("input8.txt")
    part2_bf("input8_test.txt")
    part2_bf("input8.txt")
