import pygame

pygame.init()

#первоначальная проверка. Проверяет верно ли заполнено первоначальное поле судоку
def initial_chek(lst):
    lst_turn = turn(lst)
    for y in lst:
        for x in (set(y)-{0}):
            if y.count(x)>1:
                return False
    for y in lst_turn:
        for x in (set(y)-{0}):
            if y.count(x)>1:
                return False
    return True
#проверка. Поверяет наличие нулей в строчках
def chek(lst):
   for y in lst:
      if len(set(y)-{0})<9:
         return False
   else:
      return True

def turn(lst):
   lst_turn=[[lst[y][x] for y in range(9)] for x in range(9)]
   return lst_turn

def get_gv(lst, y,x):
    g=set(lst[y])
    v=set(turn(lst)[x])
    return g,v

def get_digit_sector(lst, y,x):
    sector = [(j, i) for j in [0, 1, 2] for i in [0, 1, 2]]
    block = {}
    n = 1
    for j in [0, 3, 6]:
        for i in [0, 3, 6]:
            a = [g for k in range(3) for g in lst[j + k][i:i + 3]]
            block[n] = set(a) - {0}
            n += 1
    return block[sector.index((y//3,x//3))+1]

def get_cor_sec(y,x):
    sector = [(j, i) for j in [0, 1, 2] for i in [0, 1, 2]]
    block = {}
    n = 1
    for j in [0, 3, 6]:
        for i in [0, 3, 6]:
            a = [(j+y0,i+x0) for y0 in range(3) for x0 in range(3)]
            block[n] = a
            n += 1
    return block[sector.index((y//3,x//3))+1]

def get_var_cell(lst,y,x):
    p = {*range(1, 10)}
    g, v = get_gv(lst, y, x)
    sector = get_digit_sector(lst, y, x)
    cell = p - v - g - sector
    return cell

def get_var_sector(lst,y,x):
    sector = [(y0, x0) for y0, x0 in get_cor_sec(y, x) if lst[y0][x0] == 0]
    sector_var = [get_var_cell(lst, y0, x0) for y0, x0 in sector]
    return {cor:var for cor,var in zip(sector, sector_var)}

def min_var_cell(lst):
    l = 9
    for y in range(9):
        for x in range(9):
            if lst[y][x]==0:
                cell = get_var_cell(lst, y, x)
                if len(cell)<l and len(cell)!=0:
                    l=len(cell)
                    var_cell=cell
                    y0,x0 = y,x
    if l==9:
        return 0
    return y0,x0,list(var_cell)

def method1(lst):
    paste = 1
    while True:
        lst_line = [lst[j][i] for j in range(9) for i in range(9)]
        if 0 not in lst_line:
            break
        if paste == 0:
            return 0
        paste = 0
        for y in range(9):
            for x in range(9):
                if lst[y][x]==0:
                    cell = get_var_cell(lst,y,x)
                    if len(cell)==1:
                        lst[y][x]=cell.pop()
                        paste += 1

def method2(lst):
    paste = 1
    while True:
        lst_line = [lst[j][i] for j in range(9) for i in range(9)]
        if 0 not in lst_line:
            break
        if paste == 0:
            return 0
        paste = 0
        for y in [0,3,6]:
            for x in [0, 3, 6]:
                d = get_var_sector(lst, y, x)
                a = [j for i in d.values() for j in i]
                for k, v in d.items():
                    for i in v:
                        if a.count(i) == 1:
                            lst[k[0]][k[1]] = i
                            paste +=1

# буффер через список
def method3(lst, buffer=[]):
    try:
        y,x, var = min_var_cell(lst)
        if len(var)!=0:
            lst_copy = [[lst[y][x] for x in range(9)] for y in range(9)]
            buffer.append([lst_copy, y, x, var])
            lst[y][x] = var.pop()
    except Exception:
        y,x = buffer[-1][1],buffer[-1][2]
        var = buffer[-1][3]
        if len(var) == 0:
            buffer.pop()
            method3(lst, buffer)
        else:
            lst[:] = buffer[-1][0]
            lst[y][x]=var.pop()
            if len(var)==0:
                buffer.pop()

def solver(lst,k=0):
    lst_copy = [[lst[y][x] for x in range(9)] for y in range(9)]
    while chek(lst_copy) == False:
        m1,m2 = method1(lst_copy), method2(lst_copy)
        print(m1,m2)
        if m1 == 0 and m2 == 0:
            method3(lst_copy)
            if chek(lst_copy) == False:
                k=1
                continue
        else:
            return lst_copy,k

def DRAW_FIELD():
    [pygame.draw.rect(screen, GREY, (x+bias,y+bias,w//9,h//9),1) for x in range(0,w,w//9) for y in range(0,h,h//9)]
    [pygame.draw.rect(screen, GREY, (x+bias, y+bias, w // 3, h // 3), 3) for x in range(0, w, w // 3) for y in range(0, h, h // 3)]
    pygame.draw.rect(screen, GREY, (0+bias,0+bias,w,h),5)

def DRAW_BUTTON(screen, color,x,y,w,h, text, size):
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.SysFont('Time new roman', size)
    render= font.render(text, 1, WHITE)
    w_t,h_t = render.get_size()
    screen.blit(render, (x+(w-w_t)//2, y+(h-h_t)//2))

lst = [[0]*9 for i in range(9)]
a = []

#color
GREY = (128,128,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK_ORANGE = (211,50,0)
COLOR = {0:BLACK,1:WHITE}
black, white = 0,1
W,H = 800,800
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption('Решатель судоку')
FPS = 20

font_digit = pygame.font.SysFont('Time new roman', 55)

w,h = 540,540
cell = w//9
bias = 130
cor_surf = [(x,y) for x in range(bias,W+1-bias) for y in range(bias,H+1-bias)]
cor_button_solver= [(x,y) for x in range(250,250+130+1) for y in range(700,751)]
cor_button_clear = [(x,y) for x in range(420,420+130+1) for y in range(700,751)]
cor_button_theme =[(x,y) for x in range(5,46) for y in range(5,46)]
press_solver = True
press_clear = True
START = True
LINE = False
THEME = True
theme = True
count_line = 0
clock = pygame.time.Clock()
while True:
    screen.fill(COLOR[black])
    if THEME:
        pygame.draw.circle(screen, GREY, (25, 25), 20)
        pygame.draw.circle(screen, BLACK, (13, 18), 20)
        black, white = 0,1
    else:
        pygame.draw.circle(screen, YELLOW, (25, 25), 20)
        black,white = 1,0

    # кнопка "решить"
    if  press_solver:
        DRAW_BUTTON(screen, GREY,250,700,130,50, 'Решить',36)
    else:
        DRAW_BUTTON(screen, GREY, 251, 701, 128, 48, 'Решить', 34)
    if pygame.mouse.get_pos() in cor_button_solver:
        if press_solver:
            DRAW_BUTTON(screen, BLACK_ORANGE, 250, 700, 130, 50, 'Решить', 36)

    # # кнопка "очистить"
    if press_clear:
        DRAW_BUTTON(screen, GREY, 420, 700, 130, 50, 'Очистить', 36)
    else:
        DRAW_BUTTON(screen, GREY, 421, 700, 128, 48, 'Очистить', 34)
    if pygame.mouse.get_pos() in cor_button_clear:
        if press_clear:
            DRAW_BUTTON(screen, BLACK_ORANGE, 420, 700, 130, 50, 'Очистить', 36)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if START:
                if 48 <= event.key <= 57:
                    lst[x][y] = int(chr(event.key))
                    LINE = False
                elif event.key == pygame.K_BACKSPACE:
                    lst[x][y]=0
        if event.type == pygame.MOUSEBUTTONDOWN :
            if pygame.mouse.get_pos() in cor_button_theme and event.button == 1:
                if THEME:
                    THEME = False
                else:
                    THEME = True
            if pygame.mouse.get_pos() in cor_surf and event.button == 1:
                x, y = (event.pos[0] - bias) // cell, (event.pos[1] - bias) // cell
                LINE = True
            if pygame.mouse.get_pos() in cor_button_solver and event.button == 1:
                press_solver = False
            elif pygame.mouse.get_pos() in cor_button_clear and event.button == 1:
                press_clear = False
        if event.type == pygame.MOUSEBUTTONUP:
            if press_solver == False and event.button == 1:
                if pygame.mouse.get_pos() in cor_button_solver and event.button == 1:
                    press_solver = True
                    try:
                        if initial_chek(lst):
                            lst_slv, k = solver(lst)
                            START = False
                        else:
                            pass
                    except Exception:
                        pass
                else:
                    press_solver = True
            if press_clear == False and event.button == 1:
                if pygame.mouse.get_pos() in cor_button_clear and event.button == 1:
                    press_clear = True
                    try:
                        lst = [[0] * 9 for i in range(9)]
                        lst_slv = [[0] * 9 for i in range(9)]
                        START = True
                    except Exception:
                        pass
                else:
                    press_clear = True

    if START:
        for j in range(9):
            for i in range(9):
                if lst[j][i]!=0:
                    render_digit = font_digit.render(str(lst[j][i]), 1, COLOR[white])
                    w_d, h_d = render_digit.get_size()
                    screen.blit(render_digit, (j*cell+bias+(cell-w_d)//2,i*cell+bias+(cell-h_d)//2))

        if LINE:
            if count_line > 10:
                pygame.draw.line(screen, COLOR[white], (x * cell + bias + 55, y * cell + bias + 5),
                                 (x * cell + bias + 55, y * cell + bias + 55))
            count_line += 1
            if count_line == 20:
                count_line = 0

    else:
        [pygame.draw.rect(screen, BLACK_ORANGE, (x*cell+bias+1,y*cell+bias+1,59,59)) for x in range(9) for y in range(9) if lst[x][y]!=0]
        for j in range(9):
            for i in range(9):
                render_digit = font_digit.render(str(lst_slv[j][i]), 1, COLOR[white])
                screen.blit(render_digit, (j*cell+bias+(cell-w_d)//2,i*cell+bias+(cell-h_d)//2))
        if k==1:
            font_method = pygame.font.SysFont('Time new roman',30)
            render_method = font_method.render('УГАДАЙКА', 1, RED)
            screen.blit(render_method, (530,100))

    DRAW_FIELD()
    pygame.display.update()
    clock.tick(FPS)