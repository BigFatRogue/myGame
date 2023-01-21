import random
from SolverSudokuM12 import Sudoku, Solver


class GeneratorPole:
    def __init__(self, size: int = 9):
        self.lst = [[0] * size for y in range(size)]
        self.size = size
        self.sqrt_size = int(size**0.5)

    def get_random_sector(self):
        digit = list(range(1, self.size + 1))
        random.shuffle(digit)

        for y in range(self.sqrt_size):
            for x in range(self.sqrt_size):
                self.lst[y][x] = digit[y*self.sqrt_size + x]

    # @timer
    def run(self) -> Sudoku:
        self.get_random_sector()

        if self.size < 10:
            return Solver(self.lst).solver_random()
        return Solver(self.lst).solver()


if __name__ == '__main__':
    gen = GeneratorPole()
    res = gen.run()

    print(res)
    print(res.lst)