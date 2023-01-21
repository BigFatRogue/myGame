import cython
from collections import Counter
import random

class Sudoku:
    def __init__(self, list lst, flag_copy=False, dict cor_sec=None):
        self.lst = lst

        if not flag_copy:
            self.__check_lst(self.lst)

        self.size = len(lst)
        self.sqrt_size = int(self.size ** 0.5)
        self.cor_sector = self.get_cor_all_sector() if cor_sec is None else cor_sec
        self.variant = None

    @staticmethod
    def __check_lst(list lst):
        cpdef int l = len(lst)
        cpdef list lst_turn = [[lst[y][x] for y in range(l)] for x in range(l)]

        for obj in (lst, lst_turn):
            for row in obj:
                row = Counter(row)
                for cell, count in row.items():
                    if cell != 0:
                        if count > 1:
                            raise ValueError('Присутствуют дубликаты')

    def check(self):
        for row in self.lst:
            if 0 in row:
                return False
        return True

    def get_row(self, int row):
        cdef list digit = [i for i in self.lst[row] if i != 0]
        return set(digit)

    def get_col(self, int col):
        cdef list digit = [self.lst[y][col] for y in range(self.size) if self.lst[y][col] != 0]
        return set(digit)

    def get_cor_all_sector(self):
        cdef int s = 0
        cdef dict dct = {}

        for y in range(0, self.size, self.sqrt_size):
            for x in range(0, self.size, self.sqrt_size):
                dct[s] = [(dy, dx) for dy in range(y, y + self.sqrt_size) for dx in range(x, x + self.sqrt_size)]
                s += 1
        return dct

    def get_cor_sector(self, int y, int x):
        cdef int s = y // self.sqrt_size * self.sqrt_size + x // self.sqrt_size
        return self.cor_sector[s]

    def get_sector(self, int y, int x):
        cdef list digit = [self.lst[dy][dx] for dy, dx in self.get_cor_sector(y, x)]
        return set(digit)

    def copy(self):
        cdef list lst = [[cell for cell in row] for row in self.lst]
        return self.__class__(lst, True, cor_sec=self.cor_sector)

    def __getitem__(self, item):
        return self.lst[item]

    def __setitem__(self, key, value):
        self.lst[key] = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.lst == other.lst
        raise TypeError('Для сравнения можно передать только объект Sudoku')

    def __str__(self):
        return '\n'.join(['  '.join(map(str, row)) for row in self.lst]) + '\n'

    def __repr__(self):
        return str(self.lst)

class Solver:
    def __init__(self, list lst):
        self.lst = Sudoku(lst)

        self.buffer = []
        self.lst_solvers = []

    def get_var_cell(self, int y, int x):
        h, v, s = self.lst.get_row(y), self.lst.get_col(x), self.lst.get_sector(y, x)
        return {*range(1, self.lst.size + 1)} - h - v - s

    def get_var_sector(self, int y, int x):
        cdef list lst = []
        cdef dict dct = {}

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
        cpdef int len_min_var = self.lst.size
        cpdef tuple min_var = None

        for y, row in enumerate(self.lst):
            for x, cell in enumerate(row):
                if cell == 0:
                    var = self.get_var_cell(y, x)
                    if len(var) < len_min_var:
                        len_min_var = len(var)
                        min_var = (list(var), (y, x))

        return min_var

    def method(self):
        cdef int work = 0
        cdef int paste = 1

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

    def method_3(self):
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

    def solver(self):
        while not self.lst.check():
            m = self.method()

            if not m:
                self.method_3()

        return self.lst

    def solver_random(self):
        while not self.lst.check():
            self.get_min_var_cell()
            self.method_3()

        return self.lst

    def run_all_variant(self):
        while True:
            try:
                self.solver()

                if self.lst not in self.lst_solvers:
                    self.lst_solvers.append(self.lst)
                self.lst = self.buffer.pop()

            except IndexError:
                break

        return self.lst_solvers

    def run(self):
        self.solver()
        return self.lst