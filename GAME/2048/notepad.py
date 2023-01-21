import pygame as pg

pg.init()

RES = W, H = (600, 600)
screen = pg.display.set_mode(RES)
fps = 30

cell = 100

RECTS = [[pg.Rect(dx, dy, cell, cell), 'grey'] for dx in range(0, W, W // 4) for dy in range(0, H, H // 4)]

clock = pg.time.Clock()
while True:
    screen.fill('black')

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            for rect, color in RECTS:
                if rect.collidepoint(pg.mouse.get_pos()):
                    if color == 'grey':
                        RECTS[RECTS.index([rect, color])][1] = '#fffe44'
                    else:
                        RECTS[RECTS.index([rect, color])][1] = 'grey'

    for rect, color in RECTS:
        pg.draw.rect(screen, color, rect)

    clock.tick(fps)
    pg.display.update()
