'''Генератор головоломки'''
from draw import print_draw
import random
import itertools
from solver_sudoku import *
from generator_field import sudoku

def get_my_sud(d,n):
    with open(f'my_sudoku\my_sudoku_{d}.txt','r') as txt:
        s = txt.readlines()[n-1]
    s = s.split('@')
    lst=[int(i) for i in s[1] if i.isdigit()]
    lst_solver = [int(i) for i in s[0] if i.isdigit()]
    lst=[[lst[y * 9 + x] for x in range(9)] for y in range(9)]
    lst_solver = [[lst_solver[y * 9 + x] for x in range(9)] for y in range(9)]
    return lst,lst_solver

def get_random_sud():
    n = [*range(0, 60000)]
    with open('result.txt') as txt:
        s = txt.readlines()[random.choice(n)]
        # s = txt.readline().strip()
    s=[int(i) for i in s if i.isdigit()]
    gen=[[s[y * 9 + x] for x in range(9)] for y in range(9)]
    return gen

def cross(lst):
    cor = [(y, x) for y in range(9) for x in range(9)]
    random.shuffle(cor)
    for y,x in cor:
        lst_after = [[lst[y][x] for x in range(9)] for y in range(9)]
        lst[y][x]=0
        lst_before = [[lst[y][x] for x in range(9)] for y in range(9)]
        if chek(solver_simple(lst)):
            lst [:] = [[lst_before[y][x] for x in range(9)] for y in range(9)]
        else:
            lst [:] = [[lst_after[y][x] for x in range(9)] for y in range(9)]


def generator_sudoku():
    nice = []
    A  = []
    lst = get_random_sud()
    for i in range(1,101):
        lst_copy = [[lst[y][x] for x in range(9)] for y in range(9)]
        cross(lst)
        b = [lst[y][x] for y in range(9) for x in range(9)]
        n=81 - b.count(0)
        if n==21:
            nice.append(lst)
        if i%20==0:
            print(n, end='\n')
        else:
            print(n, end=' ')
        if lst not in A:
            A.append(lst)
        lst = [[lst_copy[y][x] for x in range(9)] for y in range(9)]
    print(nice)
    print(len(A))

# Генерирует судоку с заданной сложностью d (количество цифр в остатке) и заданное количество судоку
# сохроняет всё в соответствующий файл my_sudoku_{d}.txt
#сохраняет поле с которого генерировал и через @ саму головоломку
def generator_sudoku_in_file(d,q):
    with open(f'my_sudoku\my_sudoku_{d}.txt','a') as txt:
        count=0
        while count!=q:
            lst = get_random_sud()
            for i in range(17):
                lst_copy = [[lst[y][x] for x in range(9)] for y in range(9)]
                cross(lst)
                b = [lst[y][x] for y in range(9) for x in range(9)]
                n=81 - b.count(0)
                if n<=d:
                    txt.write(str(lst_copy) + '@')
                    txt.write(str(lst)+'\n')
                    count+=1
                    print('Нашёл')
                    lst = [[lst_copy[y][x] for x in range(9)] for y in range(9)]
                else:
                    lst = [[lst_copy[y][x] for x in range(9)] for y in range(9)]
                if count==q:
                    break

def find(lst):
    cor = [(y,x) for y in range(9) for x in range(9) if lst[y][x]!=0]
    lst_copy = [[lst[y][x] for x in range(9)] for y in range(9)]
    count = 0
    for y,x in cor:
        count +=1
        lst[y][x]=0
        print(count, end='. ')
        a=solver_all_var(lst)
        print(f'Количество решений:{a} y:{y}, x:{x}')
        lst = [[lst_copy[y][x] for x in range(9)] for y in range(9)]

#получение всех цифр для каждого сектора
def get_digit_sec(lst):
    cor_digit = {}
    for y_sec in [0, 3, 6]:
        for x_sec in [0, 3, 6]:
            a=[0 for i in range(9)]
            for y in range(3):
               for x in range(3):
                  a[y*3+x]=lst[y+y_sec][x+x_sec]
            cor_digit[(y_sec,x_sec)] = a
    return cor_digit

#вставка блока 3х3 в указанное место. В какой список вставлять, что вставлять (линейная форма) и куда вставлять.
def add_diginsec(lst,list_digit, y_sec,x_sec):
    for y in range(3):
        for x in range(3):
            lst[y+y_sec][x+x_sec]=list_digit[y*3+x]

#получение  остатков цифр для каждого сектора и их возможных перестановок
def get_combo(lst_combo):
    C = list(set(itertools.permutations(lst_combo)))
    sector_cor = [(y, x) for y in [0, 3, 6] for x in [0, 3, 6]]
    d = []
    for Comdinatiot in C:
        Comdinatiot_cor = {cor: com for cor, com in zip(sector_cor, Comdinatiot)}
        d.append(Comdinatiot_cor)
    return d

class Permutation:
    def p1(self,lst):
        all_var = []
        for a in range(9):
            zeros = [0] * 9
            zeros[a]=lst[a]
            all_var.append(zeros)
        return all_var, len(all_var)

    def p2(self, lst):
        all_var = []
        for a in range(8):
            for b in range(a + 1, 9):
                zeros = [0] * 9
                zeros[a] = lst[a]
                zeros[b] = lst[b]
                all_var.append(zeros)
        return all_var, len(all_var)

    def p3(self,lst):
        all_var = []
        for a in range(7):
            for b in range(a + 1, 8):
                for c in range(b + 1, 9):
                    zeros = [0] * 9
                    zeros[a] = lst[a]
                    zeros[b] = lst[b]
                    zeros[c] = lst[c]
                    all_var.append(zeros)
        return all_var, len(all_var)

    def p4(self,lst):
        all_var = []
        for a in range(6):
            for b in range(a + 1, 7):
                for c in range(b + 1, 8):
                    for d in range(c + 1, 9):
                        zeros = [0] * 9
                        zeros[a] = lst[a]
                        zeros[b] = lst[b]
                        zeros[c] = lst[c]
                        zeros[d] = lst[d]
                        all_var.append(zeros)
        return all_var, len(all_var)

def pere(lst):
    Permut = Permutation() #иницилизация всех возможных вариантов цифр в секторе
    lst_save = [[lst[y][x] for x in range(9)] for y in range(9)]

    giv_combo = [3,3,3,3,3,3,1,1,1] #заданный вариант остатка цифр
    Com_sector = get_combo(giv_combo) #получаем все остатки для каждого сектора
    random.shuffle(Com_sector)
    sector_dig = get_digit_sec(lst) #получение всех цифр сектора
    sector_cor = [(y, x) for y in [0, 3, 6] for x in [0, 3, 6]] #координаты секторов

    while len(Com_sector)!=0:
        print_m(lst)
        print()
        move_sec = 0  # счётчик для движения по секторам
        lst = [[lst_save[y][x] for x in range(9)] for y in range(9)]
        buffer = []
        Comdinatiot = Com_sector.pop() #получаем комбинацию остатков
        # Comdinatiot={(0,0):3, (0,3):2, (0,6):3, (3,0):2, (3,3):4, (3,6):2, (6,0):3, (6,3):2, (6,6):3}

        while move_sec != 9:
            flag = True

            y,x = sector_cor[move_sec] #получаем координаты сектора в котором будем работать
            sector_digit = sector_dig[(y,x)] # получаем цифры сектора в котором находимся

            if Comdinatiot[(x,y)]==1:
                per, limit = Permut.p1(sector_digit)
            elif Comdinatiot[(x,y)]==2:
                per,limit = Permut.p2(sector_digit) #получаем список перебранных цифр сектора
            elif Comdinatiot[(x,y)]==3:
                per,limit = Permut.p3(sector_digit)
            else:
                per,limit = Permut.p4(sector_digit)

            count_lim= 0

            while True:
                per_list = per.pop() #двигаемся по списку возможных вставок в сектор
                add_diginsec(lst, per_list ,y,x)

                if chek(solver_simple(lst)):
                    lst_buffer = [[lst[y][x] for x in range(9)] for y in range(9)]
                    buffer.append([lst_buffer, y,x,per])

                    break
                count_lim += 1
                if count_lim==limit:
                    per = buffer[-1][3]
                    while len(per)==0:
                        buffer.pop()
                        per = buffer[-1][3]
                    random.shuffle(per)
                    lst[:] = buffer[-1][0]
                    limit = len(per)
                    count_lim = 0
                    y, x = buffer[-1][1], buffer[-1][2]
                    sector = [(j, i) for j in [0, 1, 2] for i in [0, 1, 2]]
                    move_sec = sector.index((y // 3, x // 3)) + 1
                    flag = False

            if flag:
                move_sec+=1
    else:
        print_m(lst)


lst=[[1, 8, 6, 7, 5, 3, 4, 9, 2], [9, 7, 4, 6, 2, 8, 3, 1, 5], [2, 5, 3, 9, 4, 1, 7, 8, 6], [8, 9, 2, 3, 7, 5, 1, 6, 4], [4, 1, 7, 8, 6, 2, 5, 3, 9], [6, 3, 5, 1, 9, 4, 8, 2, 7], [3, 6, 9, 4, 1, 7, 2, 5, 8], [7, 2, 8, 5, 3, 9, 6, 4, 1], [5, 4, 1, 2, 8, 6, 9, 7, 3]]
pere(lst)









