# https://adventofcode.com/2021/day/24

import re
class ALU:
    """Reference implementation of the ALU to check results."""
    def __init__(self, filename):
        self.registers = { 'w': 0, 'x': 0, 'y': 0, 'z': 0}
        op_re = re.compile("(\w*) (-?\w*) ?(-?\w*)?")
        self.program = []
        with open(filename, "r") as file:
            for l in file.readlines():
                if match := op_re.match(l):
                    opcode = match.group(1)
                    op1 = match.group(2)
                    op2 = match.group(3)
                    if opcode == "inp":
                        #start a new block
                        self.program.append([])
                    if not op1 in self.registers:
                        op1 = int(op1)
                    if len(op2) and not op2 in self.registers:
                        op2 = int(op2)
                    self.program[-1].append((opcode, op1, op2))

    def run(self, number):
        input = [int(n) for n in str(number)]
        input_ptr = 0
        for r in self.registers.keys():
            self.registers[r] = 0
 
        def get_value(argument):
            if argument in self.registers:
                return self.registers[argument]
            else:
                return argument

        for block in self.program:
            for instruction in block:
                if instruction[0] == "inp":
                    self.registers[instruction[1]] = input[input_ptr]
                    input_ptr += 1
                elif instruction[0] == "add":
                    self.registers[instruction[1]] += get_value(instruction[2])
                elif instruction[0] == "mul":
                    self.registers[instruction[1]] *= get_value(instruction[2])
                elif instruction[0] == "div":
                    self.registers[instruction[1]] //= get_value(instruction[2])
                elif instruction[0] == "mod":
                    self.registers[instruction[1]] %= get_value(instruction[2])
                elif instruction[0] == "eql":
                    self.registers[instruction[1]] = 1 if get_value(instruction[1]) == get_value(instruction[2]) else 0
                else:
                    print(f"Unhandled op: {instruction[0]} {instruction[1]} {instruction[2]}")

    def y(self): return self.registers['y']
    def z(self): return self.registers['z']

def code_block(p4, p5, p15, w, y = 0, z = 0):
    """Reimplementation of each of the code blocks in Python extracting
    the parameters on the lines that change 4, 5 and 15.

    z is a stack with base 26
    if p4 == 1: push w+p15 to z
    if p4 == 26: only does the push if w != top + p5
    """

    ### top = z.pop()
    #mul x 0, add x z, mod x 26
    x = z % 26 
    #div z p4
    z //= p4

    ### x = 0 if w == top + p5 else 1
    #add x p5
    x += p5
    #eql x w, eql x 0
    x = 0 if x == w else 1

    ### if x == 1: z.push(p15 + w)
    #mul y 0, add y 25, mul y x, add y 1, mul z y
    z *= (25*x + 1) 
    #mul y 0, add y w, add y p15, mul y x
    y = (w + p15) * x # when x == 0, nothing is added
    #add z y
    z += y
    return y, z
    
def to_stack(z):
    """Test function to debug values of z"""
    stack = []
    while z > 1:
        stack.append(z % 26)
        z = z // 26
    return list(reversed(stack))


def find_pairs(alu):
    pairs = []
    stack = []
    for b_i, block in enumerate(alu.program):
        p4 = block[4][2]
        if p4 == 26: 
            top = stack.pop()
            pairs.append((top, b_i))
        else:
            stack.append(b_i)
    return pairs

if __name__ == '__main__':
    input = ALU("input24.txt")
    test_number = 13579246899999
    input.run(test_number)

    # Test that my code_block implementation works same as the reference
    y = z = 0
    for i, b in enumerate(input.program):
        p4  = b[4][2]
        p5  = b[5][2]
        p15 = b[15][2]
        w = int(str(test_number)[i])
        y, z = code_block(p4, p5, p15, w, y, z)
    
    assert(input.y() == y)
    assert(input.z() == z)

    """To find the best number I find the pair of push pops and resolve 
    each pair to find the first value in range that succesfully push the
    value pushed"""
    pairs = find_pairs(input)
    def solve_pairs(range):
        value = 0
        for p_i, p in enumerate(reversed(pairs)):
            for i in range:
                push_p15 = input.program[p[0]][15][2]
                pop_p5 = input.program[p[1]][5][2]
                top = i + push_p15 + pop_p5
                if 1 <= top <= 9:
                    value += i*pow(10, 13 - p[0]) + top*pow(10, 13 - p[1])
                    break
        return value

    part1 = solve_pairs(range(9, 0, -1))
    input.run(part1)
    print(f"What is the largest model number accepted by MONAD? {part1} (z={input.z()})")

    part2 = solve_pairs(range(1, 10))
    input.run(part2)
    print(f"What is the smallest model number accepted by MONAD? {part2} (z={input.z()})")
        


    
