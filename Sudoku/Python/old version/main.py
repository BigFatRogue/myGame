import random
from time import time
from solver_sudoku import *
from draw import *
from generator_field import sudoku
from solver_sudoku import *


def print_m(lst):
    for y in lst:
        for x in y:
            if x==0:
                print('.', end='  ')
            else:
                print(x, end='  ')
        print()

def run(lst):
    if initial_chek(lst):
        # with open('buffer.txt','w') as txt:
        #     txt.writelines('')
        print_m(lst)
        print()

        t1 = time()
        solver(lst)
        t2 = time()
        print(chek(lst), round(t2 - t1, 5),'sec')
        print_m(lst)
    else:
        print('Неправильно составленный судоку')

def show_run(lst):
    if initial_chek(lst):
        # with open('buffer.txt','w') as txt:
        #     txt.writelines('')
        print_m(lst)
        print()

        t1 = time()
        show_solver(lst)
        t2 = time()
        print(chek(lst), round(t2 - t1, 5),'sec')
        print_m(lst)
    else:
        print('Неправильно составленный судоку')
#получение поле для судоку
def get_random_sud():
    n = [*range(0, 60000)]
    with open('result.txt') as txt:
        s = txt.readlines()[random.choice(n)]
        # s = txt.readline().strip()
    s=[int(i) for i in s if i.isdigit()]
    gen=[[s[y * 9 + x] for x in range(9)] for y in range(9)]
    return gen

#получаем судоку из файла, что скачаны с тырнета
def get_from_tirnet(k):
    with open(r'from_tirnet.txt') as txt:
        s = txt.readlines()[k]
    s=[int(i) for i in s if i.isdigit()]
    a=[[s[y * 9 + x] for x in range(9)] for y in range(9)]
    return a

# получение головоломки сгенерированных мной. Возвращает запутанную и поле с которого делал
def get_my_sud(d,n):
    with open(f'my_sudoku\my_sudoku_{d}.txt','r') as txt:
        s = txt.readlines()[n-1]
    s = s.split('@')
    lst=[int(i) for i in s[1] if i.isdigit()]
    lst_solver = [int(i) for i in s[0] if i.isdigit()]
    lst=[[lst[y * 9 + x] for x in range(9)] for y in range(9)]
    lst_solver = [[lst_solver[y * 9 + x] for x in range(9)] for y in range(9)]
    return lst,lst_solver

lst = get_my_sud(21,1)[0]
# lst = get_from_tirnet(0)
# print_m(lst)
# lst,lst_solver=get_my_sud(21,2)

# run(lst)
# show_run(lst)

# show_solver_all_var(lst)

# print_draw(lst)
# print_draw(lst_solver)

# print_draw(lst_solver)
# print_red(lst, lst_solver)

