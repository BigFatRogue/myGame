import pygame as pg
import random
import numpy as np
import copy
import PgButtonText


class Cell:
    def __init__(self, y, x, value=0):
        self.value = value              # текущие значение ячейки
        self.previous_value = value     # предыдущее значение ячейки
        self.y, self.x = y, x           # текущие координаты ячейки
        self.y0, self.x0 = y, x         # предыдущее координаты ячейки
        self.action = True              # была ли ячейка просуммирована True - нет, False - да

    def get_coord(self):
        return self.y, self.x

    def set_coord(self, y, x):
        self.y = y
        self.x = x

    def get_previous_coord(self):
        return self.y0, self.x0

    def set_previous_coord(self, y, x):
        self.y0 = y
        self.x0 = x

    def __sub__(self, other):
        return Cell(self.x, self.y, self.value - other.value)

    def __bool__(self):
        return self.value == 0

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return f'{self.value}'


class GamePole:
    def __init__(self, grid=(4, 4), game_pole=None):
        self.score = 0

        self.grid = grid

        if game_pole is None:
            self.game_pole = self.create_pole()
        else:
            self.game_pole = self.create_pole(game_pole)

    def create_pole(self, key='new'):
        rows, cols = self.grid

        if isinstance(key, str):
            game_pole = [[Cell(y, x) for x in range(cols)] for y in range(rows)]
        else:
            game_pole = [[Cell(y, x, cell.value) for x, cell in enumerate(row)] for y, row in enumerate(key)]

        return game_pole

    def show(self, params=None):
        if params is not None:
            params = []

        for row in self.game_pole:
            for cell in row:
                if params:
                    print(cell, [getattr(cell, name) for name in params], end='  ')
                else:
                    print(cell, end='  ')
            print()
        print()

    def get_coord_free_cell(self):
        return [(y, x) for y, row in enumerate(self.game_pole) for x, value in enumerate(row) if value.value == 0]

    def step(self, rot):
        """
        :param rot: сколько поворотов на 90 градусов
        :return: game_pole после хода
        """

        def change_cell(item, check=True):
            '''
            :param item:
            :param check: необходимость проверки на то, была ли ячейка просуммирована до этого
            :return: None
            '''
            if check:
                # Если следующий ячейка не была просуммирована и значение ячейки не равно нулю
                if row[item - 1].action and row[item - 1].value != 0:
                    item -= 1
                    value = row[item].value * 2
                    previous_value = row[item].value
                    row[item].action = False
                    # cell.action = False
                    self.score += value
                else:
                    value = cell.value
                    previous_value = cell.value
            else:
                value = cell.value
                previous_value = cell.value

            row[item].value = value
            cell.value = 0
            cell.previous_value = previous_value
            cell.set_previous_coord(*row[item].get_coord())

        before_game_pole = copy.deepcopy(self.game_pole)

        self.game_pole = np.rot90(self.game_pole, rot)

        for y, row in enumerate(self.game_pole):
            for x, cell in enumerate(row[1:], 1):
                if cell.value != 0:

                    # Если текущая ячейки и следующая равны
                    if cell.value == row[x - 1].value:
                        change_cell(item=x)

                    # Если следующая ячейка равна нулю
                    elif row[x - 1].value == 0:
                        while row[x - 1].value == 0 and x != 0:
                            x -= 1

                        # Если текущая и следующая ячейки равны, но следующая ячейка не граничная
                        if x != 0 and cell.value == row[x - 1].value:
                            change_cell(item=x)
                        else:
                            change_cell(item=x, check=False)

        # [setattr(cell, 'action', True) for row in self.game_pole for cell in row]

        self.game_pole = np.rot90(self.game_pole, -rot)

        return GamePole(game_pole=before_game_pole)

    def check_end_game(self):
        '''
        Проверяет остались ли ходы. Просто проверяет наличие пар (value, value)
        :return: False - не осталось, True - остались
        '''
        row, col = self.grid

        rows = self.game_pole
        cols = [[self.game_pole[y][x] for y in range(row)] for x in range(col)]

        for lst in (cols, rows):
            for line in lst:
                for i, v in enumerate(line[:-1]):
                    if v.value == line[i + 1].value:
                        return False
        return True

    def get_score(self):
        return self.score

    def reset_action(self):
        [setattr(cell, 'action', True) for row in self.game_pole for cell in row]

    def reset_coord(self):
        '''
        Сбрасывает предыдущие координаты и значения
        :return: None
        '''
        for y, row in enumerate(self.game_pole):
            for x, cell in enumerate(row):
                cell.set_previous_coord(y, x)
                cell.previous_value = 0

    def __getitem__(self, item):
        return self.game_pole[item]

    def __setitem__(self, key, value):
        self.game_pole[key] = value

    def __sub__(self, other):
        lst = [[cell1 - cell2 for cell1, cell2 in zip(row1, row2)] for row1, row2 in zip(self.game_pole, other)]
        return GamePole(game_pole=lst)

    def __eq__(self, other):
        return all(cell1 == cell2 for row1, row2 in zip(self.game_pole, other) for cell1, cell2 in zip(row1, row2))

    def __bool__(self):
        return self.check_end_game()


class Game2048:
    def __init__(self):
        self.menu_w, self.menu_h = 500,75
        self.RES = self.W, self.H = self.menu_w, self.menu_w + self.menu_h
        self.screen = pg.display.set_mode(self.RES)

        self.color_background = (187, 173, 160)
        self.color_rect = (205, 193, 180)
        self.flag_end_game = False
        self.flag_siting = False
        self.end_score = 0
        self.FPS = 60

        self.grid = (2, 2)
        self.start_game()

    def start_game(self):
        self.init_surface()
        self.init_cell()
        self.init_game_pole()
        self.init_menu()

    def end_game(self):
        self.end_score = self.game_pole.get_score()

        self.init_game_pole()
        self.flag_end_game = True

    def init_game_pole(self):
        self.game_pole = GamePole(grid=self.grid)

        self.coords_grid, self.coords_grid_line = self.get_coord_grid(self.surf_w, self.surf_h)

        rows, cols = self.grid
        y, x = random.choices([(y, x) for y in range(rows) for x in range(cols)])[0]
        self.game_pole[y][x].value = self.random_digit()

    def init_cell(self, size_cell=None):
        self.color_rect = {0: (205, 193, 180), 2: (238, 228, 218), 4: (237, 224, 200), 8: (243, 178, 122),
                           16: (246, 150, 100),
                           32: (247, 124, 95), 64: (247, 95, 59), 128: (237, 208, 115), 256: (237, 204, 98),
                           512: (237, 201, 80),
                           1024: (237, 197, 63), 2048: (237, 194, 46)}

        rows, cols = self.grid
        w, h = self.surf_w, self.surf_h

        if size_cell is None:
            self.ry = h // rows * 0.93
            self.rx = w // cols * 0.93
        else:
            self.ry = size_cell[0]
            self.rx = size_cell[1]

        self.size_font = int(21 * self.ry / 30)
        self.dct_digit_render = self.render_digit(self.size_font)

    def init_surface(self):
        self.surf_res = self.surf_w, self.surf_h = int(self.W * 0.95), int(self.W * 0.95)
        x0 = self.W // 2 - self.surf_w // 2
        y0 = self.H // 2 - self.surf_h // 2 + self.menu_h//2
        self.surf_x0y0 = (x0, y0)

        self.surface = pg.surface.Surface(self.surf_res)
        self.surface.fill(self.color_background)

    def init_menu(self):
        self.font = PgButtonText.PgText(style='Clear Sans', size=25, color='white')

        self.score, *_ = self.font('SCORE')
        txt_ng, *_ = self.font('NEW GAME')

        (x, y), w, h = self.surf_x0y0, self.rx, 40
        self.b1 = PgButtonText.PgButton(surface=self.screen, color='#8F8173', rect=(x, y-70, w, h), text=txt_ng, border_radius=5)
        self.b1.action_leave(color='#635649')
        self.b1.action_click(command=self.end_game)

        txt_sit, *_ = self.font('SITTING')
        self.b2 = PgButtonText.PgButton(surface=self.screen, color='#8F8173', rect=(x+w+15, y-70, w, h), text=txt_sit, border_radius=5)
        self.b2.action_leave(color='#635649')
        self.b2.action_click(command= lambda: setattr(self, 'flag_siting', True))

        self.surface_end_game = PgButtonText.PgSurface((self.W, self.H), (0, 0))

        self.font_end_game = PgButtonText.PgText(style='Clear Sans', size=40)
        self.txt_eg1 = self.font_end_game(f'END GAME')
        self.txt_eg2 = self.font_end_game(f'YOUR SCORE')

        txt_play, *_ = self.font('PLAY')
        self.b_play = PgButtonText.PgButton(surface=self.screen, text=txt_play, color='#8F8173', rect=(100, 100, 100, 50),
                                            border_radius=5)
        self.b_play.action_leave(color='#635649')
        self.b_play.action_click(command=self.set_grid)

        self.font_text_box = PgButtonText.PgText(style='Clear Sans', size=40, color='white')
        self.text_text_box1 = self.font_text_box(str(self.grid[0]))
        self.text_box1 = PgButtonText.PgTextBox(self.screen, (150, 150), text=self.text_text_box1, width_box=50, color='#8F8173',
                                                border_radius=10, align_text='center')
        self.text_box1.action_leave(color='#635649')

        self.text_text_box2 = self.font_text_box(str(self.grid[1]))
        self.text_box2 = PgButtonText.PgTextBox(self.screen, (200, 150), text=self.text_text_box2, width_box=50, color='#8F8173',
                                                border_radius=10, align_text='center')
        self.text_box2.action_leave(color='#635649')

    @staticmethod
    def render_digit(font_size):
        pg.font.init()

        dct = {}
        for i in range(0, 25):
            number = 2 ** i

            if number in (2, 4):
                color = 'black'
            else:
                color = 'white'

            if 100 < number < 1000:
                size = int(font_size * 0.9)
            elif 1000 < number < 10000:
                size = int(font_size * 0.8)
            else:
                size = font_size

            font = pg.font.SysFont('Clear Sans', size)
            render = font.render(str(number), True, color)
            dct[number] = (render, render.get_size())

        return dct

    def move(self, rot):
        '''
        Действие при нажатии клавиш движения
        :param rot: количество поворотов на 90 градусов (+против часовой, - против)
        :return:
        '''

        # Предыдущее игровое поле
        self.before_game_pole = self.game_pole.step(rot)

        # Если поле после хода не равно предыдущему игровому полю
        if self.game_pole != self.before_game_pole:
            option_cell = self.game_pole.get_coord_free_cell()

            # Если есть ходы
            if option_cell:
                y, x = random.choices(option_cell)[0]
                self.game_pole[y][x].value = self.random_digit()
        else:
            if self.game_pole:
                self.end_game()

        # Формируется двумерный список из значений, у которых текущее положение и предыдущие равны
        # Необходим на момент отрисовки анимации
        lst_freeze = [[Cell(y,x) for x in range(self.grid[1])] for y in range(self.grid[0])]

        for y, row1, row2 in zip(range(self.grid[1]), self.game_pole, self.before_game_pole):
            for x, cell1, cell2 in zip(range(self.grid[0]), row1, row2):
                if cell1.get_coord() == cell1.get_previous_coord():
                    lst_freeze[y][x] = self.before_game_pole[y][x]

        return lst_freeze

    def get_coord_move(self):
        '''
        Получение массива состоящего из координат прямоугольника для отрисовки движения
        :return: list
        '''
        max_len = 0
        lst_render = []
        speed = int((self.H+self.W)//2*0.1)

        for y, row in enumerate(self.game_pole):
            for x, cell in enumerate(row):
                p0 = y0, x0 = cell.get_coord()              # откуда
                p1 = y1, x1 = cell.get_previous_coord()     # куда

                if p0 != p1:
                    rect0 = pos_y0, pos_x0, ry, rx = self.coords_grid[y0][x0]
                    rect1 = pos_y1, pos_x1, ry, rx = self.coords_grid[y1][x1]

                    if int(x0) > int(x1):
                        t = [(cell.previous_value, pos_y0, x, ry, rx) for x in range(pos_x0, pos_x1, -speed)]
                    elif int(x0) < int(x1):
                        t = [(cell.previous_value, pos_y0, x, ry, rx) for x in range(pos_x0, pos_x1, speed)]
                    elif int(y0) > int(y1):
                        t = [(cell.previous_value, y, pos_x0, ry, rx) for y in range(pos_y0, pos_y1, -speed)]
                    elif int(y0) < int(y1):
                        t = [(cell.previous_value, y, pos_x0, ry, rx) for y in range(pos_y0, pos_y1, speed)]

                    # Последня точка равна точки направления
                    t[-1] = (cell.previous_value, *rect1)

                    lst_render.append(t)

                    if len(t) > max_len:
                        max_len = len(t)

        # Недостающие элементы для точек, которые меньше, чем самый длинный список.
        # Доставляется из значений последний точки данного списка
        for i in lst_render:
            if len(i) < max_len:
                i += [i[-1]] * (max_len - len(i))

        # if not cell.action:
        #     anim_rect = [(d, y, x, ry + (10 * i), rx + (10 * i)) for i, (d, y, x, ry, rx) in enumerate(t[-6:])]
        #     print(anim_rect)
        #     t[-6:] = anim_rect

        # Транспортировка массива
        render = [[lst_render[y][x] for y in range(len(lst_render))] for x in range(max_len)]
        # [print(i, end='\n') for i in render]
        self.game_pole.reset_action()
        return render

    def control(self, event: pg.event.get):
        rot = None
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_UP, pg.K_w, pg.K_DOWN, pg.K_s, pg.K_LEFT, pg.K_a, pg.K_RIGHT, pg.K_d):
                if event.key in (pg.K_UP, pg.K_w):
                    rot = 1
                elif event.key in (pg.K_DOWN, pg.K_s):
                    rot = -1
                elif event.key in (pg.K_LEFT, pg.K_a):
                    rot = 0
                elif event.key in (pg.K_RIGHT, pg.K_d):
                    rot = 2
        if event.type == pg.MOUSEBUTTONDOWN:
            self.flag_end_game = False
            # self.flag_siting = False

        return rot

    @staticmethod
    def random_digit():
        """
        :return: 2 or 4
        """
        lst = [2, 2, 2, 2, 2, 2, 4, 4, 4, 4]
        indx = random.randint(0, 9)
        return lst[indx]

    def get_coord_grid(self, w, h):
        """
        :param grid: кол-во ячеек по высоте и ширине
        :param size_cell: размер ячейки (высота, широта)
        :return: координаты левого верхнего угла ячейки,высота, широта ячейки
        """
        rows, cols = self.grid
        ry, rx = self.ry, self.rx

        ky = (ry + (h - ry * rows) // (rows - 1))
        kx = (rx + (w - rx * cols) // (cols - 1))

        lst = [[0] * cols for i in range(rows)]
        line_lst = []
        for i, y in enumerate(range(rows)):
            y = int(y * ky)
            for j, x in enumerate(range(cols)):
                x = int(x * kx)
                line_lst.append((y, x, ry, rx))
                lst[i][j] = (y, x, ry, rx)

        return lst, line_lst

    def animation(self, surface, render):
        if len(render) > 0:
            lst = render.pop(0)
            [self.draw_cell(surface, (x0, y0, rx, ry), digit=d) for d, y0, x0, ry, rx in lst]
            return True

        if len(render) == 0:
            self.game_pole.reset_coord()
            return False

    def set_grid(self):
        row, col = int(self.text_box1.get_text()), int(self.text_box2.get_text())
        self.flag_siting = False
        self.grid = (row, col)
        self.start_game()

    def draw_menu(self, surface):
        self.b1.draw()
        self.b2.draw()

        w,h = self.score.get_size()
        pg.draw.rect(self.screen, '#8F8173', (390, 10, w+40, h+50), border_radius=5)
        surface.blit(self.score, (400, 20))

        txt, *_ = self.font(f'{self.game_pole.get_score()}')
        surface.blit(txt, (400, 50))

    def draw_end_game(self):
        self.txt_eg3 = self.font_end_game(str(self.end_score))

        self.surface_end_game.fill('#EDE0C8')
        self.surface_end_game.set_alpha(200)

        for i, txt in enumerate((self.txt_eg1, self.txt_eg2, self.txt_eg3)):
            t, *_ = txt
            x, y = self.W//2 - t.get_size()[0]//2, self.H//3 - t.get_size()[1]//2 + t.get_size()[1]*2*i
            self.surface_end_game.blit(t, (x, y))

        self.screen.blit(self.surface_end_game, self.surface_end_game.position)

    def draw_siting(self):
        self.surface_end_game.fill('#EDE0C8')
        self.surface_end_game.set_alpha(200)

        self.screen.blit(self.surface_end_game, self.surface_end_game.position)
        self.b_play.draw()
        self.text_box1.draw()
        self.text_box2.draw()

    @staticmethod
    def draw_grid(surface, coords, color=(205, 193, 180), radius=5):
        """
        Отрисовка сетки игрового поля
        :param surface: поверхность отрисовки
        :param color: цвет
        :param radius: радиус скругление
        :return: None
        """
        for y, x, ly, lx in coords:
            pg.draw.rect(surface, color, (x, y, lx, ly), border_radius=radius)

    def draw_cell(self, surface, rect: tuple, digit=2, radius=5):
        """
        Метод рисует заданную цифру в прямоугольнике по заданным координатам
        :param surface: поверзность отрисовки
        :param rect: (x,y,w,h)
        :param digit: число
        :param color_rect: цвет прямоугольника
        :param color_digit: цвет цифры
        :param radius: радиус скругления прямоугольника
        :return: None
        """

        x, y, lx, ly = rect

        color_rect = self.color_rect[digit]
        pg.draw.rect(surface, color_rect, rect, border_radius=radius)

        if digit != 0:
            digit_render, (w, h) = self.dct_digit_render[digit]
            surface.blit(digit_render, (x + lx // 2 - w // 2, y + ly // 2 - h // 2))

    def draw_pole(self, surface, pole, coord):
        """
        Отрисовка игрового поля
        :param surface: поверхность отрисовки
        :param pole: игровое поле (вумерный список)
        :param coords: двумерный список; (y,x,h,w) - координаты ячейки и высота и ширина
        :return: None
        """
        for y, row in enumerate(pole):
            for x, cell in enumerate(row):
                if not cell:
                    y0, x0, h, w = coord[y][x]
                    self.draw_cell(surface, (x0, y0, w, h), cell.value)

    def draw(self):
        render = []

        clock = pg.time.Clock()
        while True:
            self.screen.fill(self.color_background)
            self.surface.fill(self.color_background)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                self.b1.click(event)
                self.b2.click(event)
                self.text_box1.click(event)
                self.text_box2.click(event)
                self.b_play.click(event)

                rot = self.control(event)

                if rot is not None and len(render) == 0:
                    freeze_cell = self.move(rot)
                    render = self.get_coord_move()

            self.draw_grid(self.surface, self.coords_grid_line)

            if self.animation(self.surface, render):
                self.draw_pole(self.surface, freeze_cell, self.coords_grid)
            else:
                self.draw_pole(self.surface, self.game_pole, self.coords_grid)

            self.screen.blit(self.surface, self.surf_x0y0)

            self.draw_menu(self.screen)

            if self.flag_end_game:
                self.draw_end_game()
            if self.flag_siting:
                self.draw_siting()

            pg.display.update()
            clock.tick(self.FPS)
            pg.display.set_caption(f'2048   {int(clock.get_fps())}')

    def run(self):
        self.draw()

if __name__ == '__main__':
    game = Game2048()
    game.run()
