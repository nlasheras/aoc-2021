# https://adventofcode.com/2021/day/20

from functools import reduce
from typing import Tuple

class ImageEnhancement:
    """Class to represent the algorithm (the 512 pixels of the input)"""
    def __init__(self, pixels):
        self.pixels = pixels
        assert len(pixels) == 512

    def get(self, idx):
        assert 0 <= idx < 512
        return self.pixels[idx]

class InfiniteImage:
    """An infinite size image represented as a set of pixels and a size"""
    def __init__(self,):
        self.pixels = set()
        self.top_left = (0,0)
        self.bottom_right = (0,0)

    # this two methods compute the bounds of the image pixels
    def __top_left__(self):
        if len(self.pixels) != 0:
            return reduce(lambda acc, p: (min(p[0], acc[0]), min(p[1], acc[1])), self.pixels)
        return self.top_left

    def __bottom_right__(self):
        if len(self.pixels) != 0:
            return reduce(lambda acc, p: (max(p[0], acc[0]), max(p[1], acc[1])), self.pixels)
        return self.bottom_right

    def render(self) -> str:
        top_left = self.__top_left__()
        bottom_right = self.__bottom_right__()
        render = ""
        for j in range(top_left[1], bottom_right[1] + 1):
            for i in range(top_left[0], bottom_right[0] + 1):
                render += "#" if (i,j) in self.pixels else "."
            render += "\n"
        return render

def parse_input(filename) -> Tuple[InfiniteImage, ImageEnhancement]:
    with open(filename, "r", encoding="utf-8") as file:
        lines = [l.rstrip() for l in file.readlines()]
        algo = ImageEnhancement(lines[0])

        image = InfiniteImage()
        row = 0
        for line in lines[2:]:
            col = 0
            for char in line.rstrip():
                if char == '#':
                    image.pixels.add((col, row))
                col += 1
            row += 1

        image.top_left = (0, 0)
        image.bottom_right = (row-1, col-1)

        return image, algo

class ImageView:
    """A view to a section of the InfiniteImage hardcoded to a 3x3 area"""
    def __init__(self, image, pos, outside_value = '.'):
        self.pos = pos
        self.length = 9
        self.image = image
        self.outside_value = outside_value

    def get(self, idx):
        row = (idx // 3) - 1
        col = (idx % 3) - 1
        pixel = (self.pos[0]+col, self.pos[1]+row)
        if pixel in self.image.pixels:
            return '#'
        if (self.image.top_left[0] <= pixel[0] < self.image.bottom_right[0]) and \
             (self.image.top_left[1] <= pixel[1] < self.image.bottom_right[1]):
            return '.' # part of the image
        return self.outside_value

    def render(self):
        render = ""
        for i in range(self.length):
            value = self.get(i)
            render += value if value is not None else "."
        return render

def enhance_pass(source, algo, step):
    dest = InfiniteImage()
    dest.top_left = source.top_left
    dest.bottom_right = source.bottom_right

    # compute padding: the real input has a # in the position 0, and a . in
    # the 511, so every other pass the infinite outside area will switch between
    # 9 bits on and off. For test input is not an issue since the 0 position is
    # again 0
    outside = algo.get(0) if step % 2 else "."

    for j in range(source.top_left[1]-2, source.bottom_right[1]+3):
        for i in range(source.top_left[0]-2, source.bottom_right[0]+3):
            view = ImageView(source, (i,j), outside)
            bits = 0
            for k in range(view.length):
                bit_k = view.get(k)
                bits = (bits << 1) | (1 if bit_k == '#' else 0)

            pixel = algo.get(bits)
            if pixel == '#':
                dest.pixels.add((i,j))

    # we return a new image with "tight" bounds to not grow it more than needed
    dest.top_left = dest.__top_left__()
    dest.bottom_right = dest.__bottom_right__()
    return dest

def enhance_file(filename, passes, print_result = False):
    image, algo = parse_input(filename)
    for i in range(passes):
        image = enhance_pass(image, algo, i)

    if print_result:
        print(image.render())

    count = len(image.pixels)
    print(f"How many pixels are lit in the resulting image? {count}")

if __name__ == '__main__':
    enhance_file("input20_test.txt", 2, True)
    enhance_file("input20_test.txt", 50)

    print("\n", end='')
    enhance_file("input20.txt", 2)
    enhance_file("input20.txt", 50)
