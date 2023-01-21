"""
Реализация через 3 метода, но 1 и 2 метод объединены.
Быстрее чем методы по раздельности
"""

from PoleSudoku import Sudoku
from SaveGetTxt import *
from Timer import timer
import random


class Solver:
    def __init__(self, lst: list):
        self.lst = Sudoku(lst)

        self.buffer = []
        self.lst_solvers = []

    def get_var_cell(self, y: int, x: int) -> set:
        """Получение списка вариантов цифр для ячейки:
        цифры от [1 до self.size] - [цифры по x и y] - [цифры сектора]
        """

        h, v, s = self.lst.get_row(y), self.lst.get_col(x), self.lst.get_sector(y, x)
        return {*range(1, self.lst.size + 1)} - h - v - s

    def get_var_sector(self, y: int, x: int) -> (list, dict):
        """
        Получение списка состоящего из списка возможных цифр для ячеек сектора и координат этих ячейки:
        :return:  [((y, x), var)...]
        """

        lst = []
        dct = {}
        for dy, dx in self.lst.get_cor_sector(y, x):
            if self.lst[dy][dx] == 0:
                var_cell = self.get_var_cell(dy, dx)
                lst.append(((dy, dx), var_cell))

                for v in var_cell:
                    if v not in dct:
                        dct[v] = 1
                    else:
                        dct[v] += 1

        return lst, dct

    def get_min_var_cell(self) -> tuple:
        """
        Получение координат ячейки и вариантов цифр с минимальным выбором
        :return tuple({1, 2, 3...}, (y, x))
        """

        len_min_var = self.lst.size
        min_var = None

        for y, row in enumerate(self.lst):
            for x, cell in enumerate(row):
                if cell == 0:
                    var = self.get_var_cell(y, x)
                    if len(var) < len_min_var:
                        len_min_var = len(var)
                        min_var = (list(var), (y, x))

        return min_var

    def method_1(self) -> bool:
        work = 0
        paste = 1

        while paste != 0:
            paste = 0

            for y in range(0, self.lst.size, self.lst.sqrt_size):
                for x in range(0, self.lst.size, self.lst.sqrt_size):
                    lst, dct = self.get_var_sector(y, x)

                    for (dy, dx), var in lst:
                        if len(var) == 1:
                            self.lst[dy][dx] = var.pop()
                            paste += 1
                        else:
                            for value, count in dct.items():
                                if count == 1:
                                    if value in var:
                                        self.lst[dy][dx] = value
                                        paste += 1

            work += paste

        return work != 0

    def method_2(self) -> None:
        """
        Если method_1 и method_2 не произвели вставку, вставляется рандомно-взятое значение в ячейку с минимальным
        выбором и решение продолжается. Если выбор для ячейки ещё остался, то тогда список вносится в buffer и список
        сохраняет возможный вариант вставки и если ранее выбранная ячейка не приведёт к решению, то возьмётся
        последний добавленный список в buffer и продолжится решение.
        """

        var, (y, x) = self.lst.variant if self.lst.variant else self.get_min_var_cell()

        if var:
            lst_copy = self.lst.copy()
            lst_copy.variant = (var, (y, x))
            self.buffer.append(lst_copy)
            self.lst[y][x] = var.pop(random.randrange(len(var)))
        else:
            lst_copy = self.buffer[-1]
            var, (y, x) = lst_copy.variant

            if var:
                self.lst = lst_copy.copy()
                self.lst[y][x] = var.pop(random.randrange(len(var)))
            else:
                self.lst.variant = None
                self.buffer.pop()

    def solver(self) -> Sudoku:
        """
        Если решение не находится через m1 и m2, то тогда запускается m3 до тек пор, пока судоку не будет решено.
        :return: решённый lst
        """

        while not self.lst.check():
            m = self.method_1()

            if not m:
                self.method_2()

        return self.lst

    def solver_random(self) -> Sudoku:
        """Решение только чисто рандомным образом"""

        while not self.lst.check():
            self.get_min_var_cell()
            self.method_2()

        return self.lst

    @timer
    def run_all_variant(self) -> list:
        """
        Находит все решения для судоку путём взятия разных вариантов из buffer, до тех пор
        пока он не станет равным нулю
        """

        self.lst.show()

        while True:
            try:
                self.solver()

                if self.lst not in self.lst_solvers:
                    self.lst_solvers.append(self.lst)
                self.lst = self.buffer.pop()

            except IndexError:
                break

        print(f'Всего решений {len(self.lst_solvers)}')
        self.lst_solvers[0].show()
        print('_'*25)

        return self.lst_solvers


    @timer
    def run(self):
        self.lst.show()
        self.solver()
        self.lst.show()

    @timer
    def run_random(self):
        self.lst.show()
        self.solver_random()
        self.lst.show()


if __name__ == '__main__':
    sud, sol = get_sudoku(20, 4)
    # sud = [[4, 7, 3, 0, 2, 0, 0, 0, 0],
    #        [5, 0, 0, 8, 0, 0, 9, 3, 0],
    #        [8, 1, 9, 0, 0, 0, 0, 7, 0],
    #        [0, 0, 6, 0, 0, 0, 0, 2, 0],
    #        [0, 0, 0, 0, 0, 4, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 8],
    #        [6, 0, 0, 0, 0, 5, 0, 0, 9],
    #        [0, 3, 0, 7, 0, 0, 0, 0, 0],
    #        [1, 5, 8, 2, 0, 3, 0, 0, 4]]

    solver = Solver(sud)
    # solver.run()
    # solver.run_random()
    solver.run_all_variant()


