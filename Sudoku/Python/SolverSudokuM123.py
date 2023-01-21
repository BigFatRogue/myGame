"""
Реализация через 3 метода. Каждый метод по отдельности.
Более медленный
"""

from PoleSudoku import Sudoku
from Timer import timer
from SaveGetTxt import *
import random


class Solver:
    # __slots__ = 'lst', 'lst_solvers', 'buffer', 'min_var'

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

    def get_var_sector(self, y: int, x: int) -> list:
        """
        Получение списка состоящего из списка возможных цифр для ячеек сектора и координат этих ячейки:
        :return:  [((y, x), var)...]
        """

        lst = []
        for dy, dx in self.lst.get_cor_sector(y, x):
            if self.lst[dy][dx] == 0:
                var_cell = self.get_var_cell(dy, dx)
                lst.append(((dy, dx), var_cell))

        return lst

    def get_min_var_cell(self):
        """Получение координат ячейки и вариантов цифр с минимальным выбором"""

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
        """
        Находит ячейку с выбором цифры равным одном
        Если за полный проход по списку self.lst не было произведено ни одной вставки, то метод завершает свою работу.
        :return: True - была произведена вставка, False - не была произведена вставка
        """

        work = 0
        paste = 1
        len_min_var = self.lst.size

        while paste != 0:
            paste = 0

            for y, row in enumerate(self.lst):
                for x, cell in enumerate(row):
                    if cell == 0:
                        var = self.get_var_cell(y, x)
                        var_copy = [i for i in var]

                        if len(var) == 1:
                            self.lst[y][x] = var.pop()
                            paste += 1

                        if len(var_copy) < len_min_var:
                            len_min_var = len(var_copy)
                            self.min_var = (var_copy, (y, x))
            work += paste

        return work != 0

    def method_2(self) -> bool:
        """
        Метод просматривает варианты для ячеек в каждом секторе и если в ячейки есть значение, которого нет ни в одной
        другой ячейки, то он вставляет её.
        :return: True - была произведена вставка, False - не была произведена вставка
        """

        work = 0
        paste = 1

        while paste != 0:
            paste = 0

            for y in range(0, self.lst.size, self.lst.sqrt_size):
                for x in range(0, self.lst.size, self.lst.sqrt_size):
                    res = self.get_var_sector(y, x)

                    dct = {}
                    for cor, var in res:
                        for v in var:
                            if v not in dct:
                                dct[v] = 1
                            else:
                                dct[v] += 1

                    for value, count in dct.items():
                        if count == 1:
                            for (dy, dx), var in res:
                                if value in var:
                                    self.lst[dy][dx] = value
                                    paste += 1

            work += paste

        return work != 0

    def method_3(self):
        """
        Если method_1 и method_2 не произвели вставку, вставляется рандомно-взятое значение в ячейку с минимальным
        выбором и решение продолжается. Если выбор для ячейки ещё остался, то тогда список вносится в buffer и список
        сохраняет возможный вариант вставки и если ранее выбранная ячейка не приведёт к решению, то возьмётся
        последний добавленный список в buffer и продолжится решение.
        """

        var, (y, x) = self.lst.variant if self.lst.variant else self.min_var

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
            m2 = self.method_2()
            m1 = self.method_1()

            if not m1 and not m2:
                self.method_3()

        return self.lst

    def solver_random(self) -> Sudoku:
        """Решение только чисто рандомным образом"""

        while not self.lst.check():
            self.get_min_var_cell()
            self.method_3()

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
        # print(self.lst_solvers)
        # [print(i, '\n') for i in self.lst_solvers]

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
    sud, sol = get_sudoku(20)
    # sud = [[3, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 3, 4, 0, 0], [0, 7, 0, 0, 9, 0, 5, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 4, 1, 0, 0, 0, 9, 0, 6], [0, 0, 0, 2, 0, 0, 0, 0, 7], [1, 0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 2, 1, 0, 0]]

    solver = Solver(sud)
    solver.run()
    # solver.run_random()
    # solver.run_all_variant()


