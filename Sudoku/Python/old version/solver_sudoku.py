import time


def print_m(lst):
    for y in lst:
        for x in y:
            if x==0:
                print('.', end='  ')
            else:
                print(x, end='  ')
        print()
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
    while chek(lst) == False:
        if method1(lst) == 0 and method2(lst) == 0:
            method3(lst)
            if chek(lst) == False:
                k=1
                continue
        else:
            if k == 1:
                print('Угадайка ')
            return lst

def show_solver(lst):
    while chek(lst) == False:
        if method1(lst) == 0 and method2(lst) == 0:
            method3(lst)
            print_m(lst)
            print()

#решатель для генерации судоку
def solver_simple(lst):
    lst_copy = [[lst[y][x] for x in range(9)] for y in range(9)]
    if method1(lst_copy) == 0 and method2(lst_copy) ==0:
        return lst_copy
    else:
        return lst_copy

def show_solver_all_var(lst,p=0):
    all_var =[]
    try:
        while chek(lst) == False:
            if method1(lst) == 0 and method2(lst) == 0:
                method3(lst)
            else:
                if lst not in all_var:
                    all_var.append([[lst[y][x] for x in range(9)] for y in range(9)])
                print_m(lst)
                print()
                p+=1
                method3(lst)
    except Exception:
        if p==0 or p==1:
            print('Только одно решение', end='  ')
        else:
            print(f'Количество решений: {p}', end='  ')
            print(len(all_var))

def solver_all_var(lst,p=0):
    all_var = []
    try:
        while chek(lst) == False:
            if method1(lst) == 0 and method2(lst) == 0:
                method3(lst)
            else:
                p+=1
                method3(lst)
            #укороченный
            if p>2:
                return '@'
    except Exception:
        if p==1:
            return 1
        else:

            return p


lst = sud = [[4, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 9, 3, 0], [0, 1, 0, 0, 0, 0, 0, 7, 0], [0, 0, 6, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 8], [6, 0, 0, 0, 0, 5, 0, 0, 9], [0, 3, 0, 7, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 3, 0, 0, 4]]

# lst_s = [[4, 8, 1, 6, 7, 5, 2, 9, 3],
#          [7, 3, 6, 8, 2, 9, 5, 4, 1],
#          [5, 2, 9, 4, 3, 1, 8, 7, 6],
#          [9, 5, 3, 1, 8, 7, 6, 2, 4],
#          [2, 4, 7, 5, 6, 3, 1, 8, 9],
#          [6, 1, 8, 9, 4, 2, 3, 5, 7],
#          [3, 7, 5, 2, 9, 6, 4, 1, 8],
#          [1, 6, 4, 7, 5, 8, 9, 3, 2],
#          [8, 9, 2, 3, 1, 4, 7, 6, 5]]
# lst = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 3, 6, 0, 0, 0, 0, 0],
#        [0, 7, 0, 0, 9, 0, 2, 0, 0],
#        [0, 5, 0, 0, 0, 7, 0, 0, 0],
#        [0, 0, 0, 0, 4, 5, 7, 0, 0],
#        [0, 0, 0, 1, 0, 0, 0, 3, 0],
#        [0, 0, 1, 0, 0, 0, 0, 6, 8],
#        [0, 0, 8, 5, 0, 0, 0, 1, 0],
#        [0, 9, 0, 0, 0, 0, 4, 0, 0]]

start = time.time()
slst = show_solver_all_var(lst)
print(lst)
end = time.time()
print(end - start, 'сек')




