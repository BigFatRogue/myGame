from collections import Counter


class Sudoku:
    def __init__(self, lst: list, flag_copy=False, cor_sec=None):
        self.lst = lst
        if not flag_copy:
            self.__check_lst(self.lst)

        self.size = len(lst)
        self.sqrt_size = int(self.size ** 0.5)
        self.cor_sector = self.get_cor_all_sector() if cor_sec is None else cor_sec

        self.variant = None

    @staticmethod
    def __check_lst(lst: list) -> None:
        'Проверка на наличие дубликатов строчке или колонке в получаемом списке'

        l = len(lst)
        lst_turn = [[lst[y][x] for y in range(l)] for x in range(l)]

        for obj in (lst, lst_turn):
            for row in obj:
                row = Counter(row)
                for cell, count in row.items():
                    if cell != 0:
                        if count > 1:
                            raise ValueError('Присутствуют дубликаты')

    def check(self) -> bool:
        'Проверяет есть ли нули в строчках. Если есть, значит судоку ещё не решено'
        for row in self.lst:
            if 0 in row:
                return False
        return True

    def get_row(self, row: int) -> set:
        'Получение множества состоящего из чисел в заданной строке списка'

        digit = [i for i in self.lst[row] if i != 0]
        return set(digit)

    def get_col(self, col: int) -> set:
        'Получение множества состоящего из чисел в заданной колонке списка'

        digit = [self.lst[y][col] for y in range(self.size) if self.lst[y][col] != 0]
        return set(digit)

    def get_cor_all_sector(self) -> dict:
        """
        Получение координат всех секторов.
        :return: {1: ((y, x),..) ... self.size: ((y, x),..)}
        """

        s = 0
        dct = {}
        for y in range(0, self.size, self.sqrt_size):
            for x in range(0, self.size, self.sqrt_size):
                rng_y = range(y, y + self.sqrt_size)
                rng_x = range(x, x + self.sqrt_size)

                dct[s] = tuple((dy, dx) for dy in rng_y for dx in rng_x)
                s += 1

        return dct

    def get_cor_sector(self, y: int, x: int) -> tuple:
        """
        Получение координат сектора по координатам.
        :return: ((y, x),..)
        """

        s = y // self.sqrt_size * self.sqrt_size + x // self.sqrt_size
        return self.cor_sector[s]

    def get_sector(self, y, x) -> set:
        'Получение множества состоящего из цифр заданного сектора'

        digit = [self.lst[dy][dx] for dy, dx in self.get_cor_sector(y, x)]

        return set(digit)

    def show(self):
        for y, row in enumerate(self.lst, 1):
            for x, cell in enumerate(row, 1):
                print(cell, end='  ')
            print()
        print()

    def copy(self):
        lst = [[cell for cell in row] for row in self.lst]
        return self.__class__(lst, flag_copy=True, cor_sec=self.cor_sector)

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


if __name__ == '__main__':
    pole = [[0, 0, 0, 0, 0, 3, 1, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 3, 0, 7, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 3], [0, 6, 0, 8, 0, 0, 5, 0, 0], [9, 8, 0, 6, 0, 0, 0, 0, 7], [0, 0, 0, 2, 0, 7, 0, 0, 6], [0, 4, 0, 0, 0, 0, 0, 0, 0], [8, 2, 1, 0, 0, 0, 0, 0, 0]]    # sud = [[0, 0, 1, 0, 0, 0, 2, 0, 0], [0, 3, 0, 0, 0, 0, 0, 4, 0], [5, 0, 0, 0, 3, 0, 0, 0, 6], [0, 0, 0, 1, 0, 7, 0, 0, 0], [0, 4, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 9, 0, 2, 0, 0, 0], [3, 0, 0, 0, 0, 0, 0, 0, 8], [0, 6, 0, 0, 5, 0, 0, 3, 0], [0, 0, 2, 0, 0, 0, 7, 0, 0]]
    sud = Sudoku(pole)
    sud.show()
