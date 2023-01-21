from GeneratorPole import GeneratorPole
from SolverSudokuM12 import Solver
# from SolverSudokuM123 import Solver
import random
import time

from Timer import timer
from SaveGetTxt import *
from WinBall import WindowsBalloonTip


class GeneratorSudoku(Solver):
    def __init__(self, lst: list, quality=21):
        super().__init__(lst)
        self.lst_copy = self.lst.copy()
        self.quality = quality

        self.lst.variant_gen = None
        self.buffer_gen = []

    def solver_for_gen(self):
        res_1 = False

        while True:
            try:
                while not self.lst.check():
                    m = self.method_1()
                    if not m:
                        self.method_2()

                if self.lst not in self.lst_solvers:
                    self.lst_solvers.append(self.lst)

                if len(self.lst_solvers) == 1:
                    res_1 = True
                elif len(self.lst_solvers) > 1:
                    res_1 = False
                    self.lst_solvers = []
                    self.buffer = []
                    break

                self.lst = self.buffer.pop()

            except IndexError:
                break

        return res_1

    @timer
    def create_sudoku(self):
        start = time.time()

        delay = 1
        count = 0
        while (self.lst.size**2 - self.quality) != count:
            coord = [(y, x) for y, row in enumerate(self.lst) for x, cell in enumerate(row) if cell != 0]
            while True:
                if coord:
                    y, x = random.choice(coord)
                else:
                    count = 0
                    self.lst = self.lst_copy.copy()
                    start = time.time()
                    break

                lst_copy = self.lst.copy()
                self.lst[y][x] = 0
                lst_zero = self.lst.copy()
                res1 = self.solver_for_gen()

                if res1:
                    count += 1
                    self.lst = lst_zero.copy()
                    break
                else:
                    coord.remove((y, x))
                    self.lst = lst_copy.copy()

                end = time.time()

                if end - start > delay:
                    count = 0
                    self.lst = self.lst_copy.copy()
                    start = time.time()
                    break

        return self.lst.lst


if __name__ == '__main__':
    win_info = WindowsBalloonTip()

    # Генерация поля
    pole = GeneratorPole().run().lst

    # Генерация головоломки
    gen = GeneratorSudoku(pole, quality=22)
    res = gen.create_sudoku()

    # Сохранение головоломки
    save_sudoku(res, pole)

    win_info.create_window('Генератор судоку', 'Готово')



