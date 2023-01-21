import numpy as np
import time
import random


def timer(func):
    def wrapper(*args):
        start = time.time()
        res = func(*args)
        end = time.time()
        print(end - start, 'сек')
        return res
    return wrapper


class Sudoku:
    __slots__ = ('lst', 'size', 'sqrt_size', 'variant', 'line_var')

    def __init__(self, lst: (list, tuple)):
        self.lst = np.array([np.array([cell for cell in row]) for row in lst])
        self.__check_lst(self.lst)
        self.size = len(lst)
        self.sqrt_size = int(self.size ** 0.5)

        self.line_var = np.array([i for i in range(1, self.size + 1)], int)
        self.variant = None

    def __check_lst(self, lst):
        for line_x, line_y in zip(lst, np.rot90(lst)):
            line_x = line_x[line_x != 0]
            line_y = line_y[line_y != 0]
            if len(np.unique(line_x)) != len(line_x) or len(np.unique(line_y)) != len(line_y):
                raise ValueError('Присутствуют дубликаты')

    def check(self) -> bool:
        'Проверяет есть ли нули в строчках. Если есть, значит судоку ещё не решено'
        for row in self.lst:
            if 0 in row:
                return False
        return True

    def get_row(self, row: int) -> np.array:
        digit = self.lst[row]
        return digit[digit != 0]

    def get_col(self, col: int) -> np.array:
        digit = self.lst[:, col]
        return digit[digit != 0]

    def get_cor_sector(self, y, x):
        y, x = y // self.sqrt_size, x // self.sqrt_size
        rng_y = y * self.sqrt_size, y * self.sqrt_size + self.sqrt_size
        rng_x = x * self.sqrt_size, x * self.sqrt_size + self.sqrt_size

        return rng_y, rng_x

    def get_sector(self, y, x) -> np.array:
        rng_y, rng_x = self.get_cor_sector(y, x)
        digit = np.array([self.lst[dy, dx] for dy in range(*rng_y) for dx in range(*rng_x)])

        return digit[digit != 0]

    def show(self):
        for row in self.lst:
            for cell in row:
                print(cell, end='  ')
            print()
        print()

    def __getitem__(self, item):
        return self.lst[item]

    def __setitem__(self, key, value):
        self.lst[key] = value


class Solver:
    def __init__(self, lst: (list, tuple)):
        self.lst = Sudoku(lst)

    def sub_var(self, var):
        return np.setdiff1d(np.array([*range(1, self.lst.size + 1)]), var)

    def get_var_cell(self, y: int, x: int) -> np.array:
        '''Получение списка вариантов цифр для ячейки:
        цифры от [1 до self.size] - [цифры по x и y] - [цифры сектора]
        '''

        h, v, s = self.lst.get_row(y), self.lst.get_col(x), self.lst.get_sector(y, x)

        var = np.unique(np.append(h, (*v, *s)))
        var = self.sub_var(var)

        return var

    def get_var_sector(self, y, x) -> np.array:
        rng_x, rng_y = self.lst.get_cor_sector(y, x)
        lst = []
        for dy in range(*rng_x):
            for dx in range(*rng_y):
                if self.lst[dy, dx] == 0:
                    var_cell = self.get_var_cell(dy, dx)
                    lst.append(((dy, dx), var_cell))
        return lst
        # sector = self.lst.get_sector(y, x)
        # for

    def method_1(self):
        paste = 1
        while paste != 0:
            paste = 0

            for y, row in enumerate(self.lst):
                for x, cell in enumerate(row):
                    if cell == 0:
                        var = self.get_var_cell(y, x)
                        if len(var) == 1:
                            self.lst[y, x] = var[0]
                            paste += 1

    def method_2(self):
        paste = 1
        while paste != 0:
            paste = 0

        for y in range(0, self.lst.size, self.lst.sqrt_size):
            for x in range(0, self.lst.size, self.lst.sqrt_size):
                res = self.get_var_sector(y, x)

                variants = np.array([], int)
                for cor, var in res:
                    variants = np.append(variants, var)

                unique, counts = np.unique(variants, return_counts=True)

                for u, c in zip(unique, counts):
                    if c == 1:
                        for (dy, dx), var in res:
                            if u in var:
                                self.lst[dy, dx] = u
                                paste += 1

    @timer
    def run(self):
        self.lst.show()

        while not self.lst.check():
            self.method_1()
            self.method_2()

        self.lst.show()


if __name__ == '__main__':
    sud = [[0, 0, 1, 0, 0, 6, 0, 0, 7],
           [4, 0, 3, 0, 8, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 2],
           [2, 9, 0, 4, 0, 0, 0, 3, 0],
           [0, 0, 0, 3, 6, 5, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 2, 0, 0, 0, 4, 0],
           [9, 0, 0, 0, 0, 0, 0, 0, 0],
           [7, 0, 0, 0, 0, 0, 5, 0, 6]]



    sol = Solver(sud)
    sol.run()
