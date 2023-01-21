'''Генерирует заполненное поле судоку'''

import random
import time

#вращение матрицы
def turn(lst):
   lst[:]=[[lst[y][x] for y in range(9)] for x in range(9)]

#проверка. Проверяет линии на наличие одинаковых цифр в них
def chek(lst):
   lst_turn = [[lst[y][x] for y in range(9)] for x in range(9)]
   for line_y,line_x in zip(lst, lst_turn):
      if len(set(line_y))<9 or len(set(line_x))<9:
         return False
   else:
      return True

#создание блока 3х3 со значениями 1-9 в случайно порядке
def add_r(lst):
   a = [*range(1, 10)]
   random.shuffle(a)
   for y in range(3):
      for x in range(3):
         lst[y][x]=a[y*3+x]

#добавляет нулевую матрицу 3х3 в указанное место массива
def add_zeros(lst,j,i):
   a=[0 for i in range(9)]
   for y in range(3):
      for x in range(3):
         lst[y+j][x+i]=a[y*3+x]

#заполнение блоков 1,2,3,4,7
def step1():
   lst = [[0] * 9 for i in range(9)]
   add_r(lst) #добавляем в позицию(первую) 0,0 рандомную матрицу 3х3
   for t in range(2): #0 - заполняем блок вправо, 1 - заполняем блок вниз
      position = ((0, 3), (0, 6))# 0-  заполняем 2 квадрат(позиция), 1 - заполняем 3 квадрат(позиция)
      if t==1:
         turn(lst)
      for n in range(2):
         y0,x0=position[n]
         y=0
         while y<3:
            if x0==6: # для 3 позиции
               s= {1,2,3,4,5,6,7,8,9}
               n1=s-set(lst[y0]) #первая линия (0,0)
               n2=s-set(lst[y0+1]) #вторая линия (1,0)
               n3 =s - set(lst[y0 + 2]) #третья линия (2,0)
            else:  # для 2 позиции
               n1 = set(lst[y0 + 1][:x0] + lst[y0 + 2][:x0]) #первая линия (0,0)
               n2 = set(lst[y0][:x0] + lst[y0 + 2][:x0])-set(lst[y0][x0:x0+3]) #вторая линия (1,0)
               n3 = set(lst[y0][:x0] + lst[y0 + 1][:x0])-set(lst[y0][x0:x0+3]+lst[y0+1][x0:x0+3]) #третья линия (2,0)
            try:
               for x in range(3):
                  d = {0: n1, 1: n2, 2: n3} #выбираем линию с которой работаем
                  dy=list(d[y]) #создаём из полуенного из словаря множество список
                  v=random.choice(dy) #выбираем случайное число из него
                  lst[y+y0][x+x0]=v #добавляем это число в матрицу
                  d[y].remove(v) #удаляем добавленное число из множества
               y+=1
            except Exception: #если не получится, то обнулим данную позицию, отойдём на шаг назад и попробуем снова
               add_zeros(lst, y0, x0)
               y=0
   return lst

#заполнение блоков 5,6
def step2():
   lst = step1()
   position = ((3, 3), (3, 6))
   for n in range(2):
      y0,x0 = position[n]
      y=0
      u=0 # счётчик прекращаения
      while y<3:
         if x0==6:
            s = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            n1 = s - set(lst[y0])  # первая линия (0,0)
            n2 = s - set(lst[y0 + 1])  # вторая линия (1,0)
            n3 = s - set(lst[y0 + 2])  # третья линия (2,0)
         else:
            n1 = set(lst[y0 + 1][:x0] + lst[y0 + 2][:x0])
            n2 = set(lst[y0][:x0] + lst[y0 + 2][:x0]) - set(lst[y0][x0:x0 + 3])
            n3 = set(lst[y0][:x0] + lst[y0 + 1][:x0]) - set(lst[y0][x0:x0 + 3] + lst[y0 + 1][x0:x0 + 3])
         try:
            for x in range(3):
               k = set([lst[y0 - 1][x0+x]] + [lst[y0 - 2][x0+x]] + [lst[y0 - 3][x0+x]])
               d = {0: n1, 1: n2, 2: n3}
               d2 = {0: d[0]-k, 1: d[1]-k, 2: d[2]-k}
               dy = list(d2[y])
               v = random.choice(dy)
               lst[y + y0][x + x0] = v
               d[y].remove(v)
            y += 1
         except Exception:  # если не получится, то обнулим данную позицию, отойдём на шаг назад и попробуем снова
            add_zeros(lst, y0, x0)
            y = 0
         u+=1
         if u>=40: #если будет равен или больше 100, то работу вернёт 0
            return 0
   return lst

#заполнение блоков 8,9
def step3(lst):
   position = ((6, 3), (6, 6))
   n=0
   y=0
   while n<1:
      if y==3:
         n += 1
      y0,x0=position[n]
      y=0
      mistake=0
      u=0
      while y<3:
         if x0==6:
            s = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            n1 = s - set(lst[y0])  # первая линия (0,0)
            n2 = s - set(lst[y0 + 1])  # вторая линия (1,0)
            n3 = s - set(lst[y0 + 2])  # третья линия (2,0)
         else:
            n1 = set(lst[y0 + 1][:x0] + lst[y0 + 2][:x0])
            n2 = set(lst[y0][:x0] + lst[y0 + 2][:x0]) - set(lst[y0][x0:x0 + 3])
            n3 = set(lst[y0][:x0] + lst[y0 + 1][:x0]) - set(lst[y0][x0:x0 + 3] + lst[y0 + 1][x0:x0 + 3])
         try:
            for x in range(3):
               k = k=set([lst[y0 - i][x0+x] for i in range(1,7)]) #массив (полоска) значений что выше
               d = {0: n1, 1: n2, 2: n3}
               d2 = {0: d[0]-k, 1: d[1]-k, 2: d[2]-k} #добавляет измененные значения при этом не меня предыдущие
               dy = list(d2[y])
               v = random.choice(dy)
               lst[y + y0][x + x0] = v
               d[y].remove(v)
            y += 1
         except Exception:
            add_zeros(lst, y0, x0)
            y = 0
            mistake+=1
            if mistake>50: # счётчик ошибок. Если выполнил n итераций то попробует заного
               n=0
               y0, x0 = position[n]
               add_zeros(lst, y0, x0)
         u+=1
         if u>=40:
            return 0
   return lst

def sudoku():
   s2=step2()
   if s2==0:
      return sudoku()
   s3=step3(s2)
   if s3==0:
      return sudoku()
   else:
      return s3

#метод для записи любого кол-ва судоку в файл result.txt
def write_sudoku(k):
   with open('result.txt','a') as txt:
      for i in range(k):
            a = sudoku()
            txt.write(str(a) + '\n')

def print_m(lst):
   for y in lst:
      for x in y:
         print(x, end='  ')
      print()
#сгенерировать поле судоко
def run():
   t1 = time.time()
   a = sudoku()
   t2 = time.time()
   print(chek(a), end=' ')
   print(round(t2 - t1, 5), 'cек')
   print_m(a)







