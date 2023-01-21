import pygame as pg


class PgText:
    def __init__(self, style='Arial', size=14, color='black', bold=False, italic=False):
        pg.font.init()
        self.__font = pg.font.SysFont(style, size, bold, italic)
        self.__style = style
        self.__size = size
        self.__color = color
        self.__bold = bold
        self.__italic = italic
        self.__render = None

    def __call__(self, string: str):
        self.__render = self.__font.render(string, True, self.__color)
        return self.__render, string, PgText(self.__style, self.__size, self.__color, self.__bold, self.__italic)


class PgBox:
    def __init__(self, surface, color, text, alpha, border_radius):
        """
        :param surface: поверхность отрисовки
        :param color: цвет объекта (leave - при наведении, click - после нажатия)
        :param text:  цвет текста (leave - при наведении, click - после нажатия)
        :param alpha: True - отрисовка прямоугольника (задника)
        :param border_radius: радиус скругления углов
        """
        self.surface = surface

        self._color = color
        self._text = text
        self._alpha = alpha
        self._border_radius = border_radius

        self._leave_color = color
        self._leave_text = text
        self._leave_border_radius = border_radius

        self._click_text = text
        self._click_color = color
        self._click_border_radius = border_radius

        self._press_b1 = False

    def action_leave(self, color=None, rect=None, border_radius=None, text=None):
        if color is not None:
            self._leave_color = color
        if rect is not None:
            self._leave_rect = pg.Rect(rect)
        if border_radius is not None:
            self._leave_border_radius = border_radius
        if text is not None:
            self._leave_text = text

    def action_click(self, color=None, rect=None, border_radius=None, text=None, command=None, args=None):
        if color is not None:
            self._click_color = color
        if rect is not None:
            self._click_rect = pg.Rect(rect)
        if border_radius is not None:
            self._click_border_radius = border_radius
        if text is not None:
            self._click_text = text


class PgSurface(pg.Surface):
    'Измененная PyGame поверхность, которая ещё возвращает свою позицию и размеры'

    def __init__(self, size: tuple, position: tuple):
        pg.Surface.__init__(self, size)
        self.__rect = (*position, *size)
        self.__size = size
        self.__position = position

    @property
    def size(self):
        return self.__size

    @property
    def position(self):
        return self.__position

    def rect(self):
        return self.__rect


class PgButton(PgBox):
    number = 0
    __press_b1 = True

    @classmethod
    def __id_button(cls):
        cls.number += 1

    def __init__(self, surface, rect: tuple, text, color='white', alpha=True, border_radius=5):
        super().__init__(surface, color, text, alpha, border_radius)

        self.__x, self.__y, self.__rx, self.__ry = rect

        if isinstance(surface, PgSurface):
            x, y = surface.position
            self.__x += x
            self.__y += y

        if not isinstance(rect, pg.Rect):
            self._rect = pg.Rect(self.__x, self.__y, self.__rx, self.__ry)

        self._leave_rect = self._rect
        self._click_rect = self._rect

        self._command = None
        self._func_complite = False

        self.__id = self.number
        self.__id_button()

    def __leave(self):
        mouse = pg.mouse
        pos = mouse.get_pos()

        if self._rect.collidepoint(pos):
            pg.draw.rect(self.surface, self._leave_color, self._leave_rect, border_radius=self._leave_border_radius)
            self.__draw_text(self._leave_text)
        else:
            self.__press_b1 = False

    def action_click(self, color=None, rect=None, border_radius=None, text=None, command=None, args=None):
        super().action_click(color, rect, border_radius, text)
        if command is not None:
            self._command = command
            self.__args = args if args is not None else ()

    def __click(self):
        if self._press_b1:
            pg.draw.rect(self.surface, self._click_color, self._click_rect, border_radius=self._click_border_radius)
            self.__draw_text(self._click_text)

            if self._command is not None and self._func_complite:
                self._command(*self.__args)
                self._func_complite = False

        return pg.mouse.get_pressed()[0]

    def click(self, event):
        mouse = pg.mouse
        pos = mouse.get_pos()

        if event.type == pg.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(pos):
                self._press_b1 = True
                self._func_complite = True
        else:
            self._press_b1 = False

    def move(self):
        mouse = pg.mouse
        pos = mouse.get_pos()
        b1 = mouse.get_pressed(3)[0]

        if self.__x < pos[0] < self.__x + self.__rx and self.__y < pos[1] < self.__y + self.__ry and b1:
            self.__x, self.__y = pos[0] - self.__rx // 2, pos[1] - self.__ry // 2
            self._rect = self._leave_rect = self._click_rect = pg.Rect(self.__x, self.__y, self.__rx, self.__ry)

    def __draw_text(self, text):
        if text is None:
            return False
        else:
            w, h = text.get_size()
            x, y = self.__x + (self.__rx // 2 - w // 2), self.__y + (self.__ry // 2 - h // 2)
            self.surface.blit(text, (x, y))
        return True

    def draw(self):
        if self._alpha:
            pg.draw.rect(self.surface, self._color, self._rect, border_radius=self._border_radius)

        self.__draw_text(self._text)

        if not self.__click():
            self.__leave()


class PgTextBox(PgBox):
    number = 1
    __press_b1 = True

    @classmethod
    def __id_box(cls):
        cls.number += 1

    def __init__(self, surface, position: tuple, text=None, width_box=25, color='white', align_text='left',
                 alpha=True, border_radius=0):
        super().__init__(surface, color, text, alpha, border_radius)

        self.__x, self.__y = position
        if isinstance(surface, PgSurface):
            x, y = surface.position
            self.__x += x
            self.__y += y

        if text is None:
            self.__string = ''
            self.__font = PgText(size=20)
            self.__text_render, *_ = self.__font(self.__string)
        else:
            self.__text_render, self.__string, self.__font = text

        self.__rx = width_box
        self.__ry = self.__text_render.get_size()[1]

        self.__rect = pg.Rect(self.__x, self.__y, self.__rx, self.__ry)

        self.__align_text = align_text

        self.c = 0  # счётчик для каретки

        self.__leave_rect = self.__rect
        self.__click_rect = self.__rect

        self.x_align, self.y_align = self.__align(self.__text_render.get_size()[0])

        self.__id = self.number
        self.__id_box()

    def get_text(self):
        return self.__string

    def set_text(self, string):
        self.__string = string

    def get_rect(self):
        return self.__rect

    def __leave(self):
        mouse = pg.mouse
        pos = mouse.get_pos()
        if self.__rect.collidepoint(pos):
            pg.draw.rect(self.surface, self._leave_color, self.__leave_rect, border_radius=self._leave_border_radius)
            return True
        return False

    def click(self, event):
        mouse = pg.mouse
        pos = mouse.get_pos()

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.__rect.collidepoint(pos):
                self._press_b1 = True
            else:
                self._press_b1 = False

        if event.type == pg.KEYDOWN:
            if self._press_b1:
                s = event.key

                if s == 8:
                    self.__string = self.__string[:-1]
                else:
                    try:
                        self.__string += str(chr(s))
                    except Exception:
                        pass

    def __align(self, w):
        if self.__align_text == 'center':
            x, y = self.__x + self.__rx // 2 - w // 2, self.__y
        elif self.__align_text == 'right':
            x, y = self.__x + self.__rx, self.__y
        else:
            x, y = self.__x * 1.03, self.__y
        return x, y

    def __draw_text(self):

        render, *_ = self.__font(str(self.__string))
        w, h = render.get_size()

        # отрисовка каретки
        if self._press_b1:
            pg.draw.rect(self.surface, self._leave_color, self.__leave_rect, border_radius=self._leave_border_radius)

            self.c += 1

            self.x_align, self.y_align = self.__align(w)

            pos0 = (self.x_align + w + 1, self.__y + h * 0.1)
            pos1 = (self.x_align + w + 1, self.__y + h * 0.9)

            if 0 < self.c < 35:
                pg.draw.line(self.surface, 'black', pos0, pos1)
            if self.c > 70:
                self.c = 0

        self.surface.blit(render, (self.x_align, self.y_align))

    def draw(self):
        if self._alpha:
            pg.draw.rect(self.surface, self._color, self.__rect, border_radius=self._border_radius)

        self.__leave()
        self.__draw_text()


if __name__ == '__main__':
    RES = W, H = 500, 500
    screen = pg.display.set_mode(RES)
    FPS = 60

    surface = PgSurface((400, 400), (0, 0))

    font = PgText('Arial', 25)
    txt_b, *_ = font('BUTTON')
    button = PgButton(surface, (0, 0, 100, 50), txt_b, color='#FF9D6D', border_radius=5)
    button.action_leave(color='#98544C')

    tb = PgTextBox(surface, position=(250, 250), width_box=100, text=font('TEXT_BOX'), color='#40B3AF')
    tb.action_leave(color='#348985')

    func = lambda: tb.set_text('b1')
    button.action_click(color='green', command=func)

    tb2 = PgTextBox(surface, position=(100, 100), width_box=100, color='#40B3AF')
    tb2.action_leave(color='#348985')

    clock = pg.time.Clock()
    while True:
        screen.fill('white')
        surface.fill('#417A70')

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            button.click(event)
            tb.click(event)
            tb2.click(event)

        button.draw()
        # button.move()

        tb.draw()
        tb2.draw()

        screen.blit(surface, surface.position)

        pg.display.update()
        clock.tick(FPS)
