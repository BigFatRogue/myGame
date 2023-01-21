from numba import njit
import numpy as np
from time import time

def print_m(lst):
    for y in lst:
        for x in y:
            if x==0:
                print('.', end='  ')
            else:
                print(x, end='  ')
        print()

# lst = [
#     [4, 3, 6, 2, 7, 1, 5, 8, 9],
#     [1, 8, 2, 3, 9, 5, 7, 6, 4],
#     [5, 9, 7, 8, 4, 6, 3, 2, 1],
#     [9, 1, 5, 6, 8, 4, 2, 7, 3],
#     [7, 4, 8, 5, 3, 2, 1, 9, 6],
#     [6, 2, 3, 9, 1, 7, 4, 5, 8],
#     [2, 7, 4, 1, 6, 9, 8, 3, 5],
#     [3, 5, 9, 4, 2, 8, 6, 1, 7],
#     [8, 6, 1, 7, 5, 3, 9, 4, 2]]

lst = np.array(
    [[4, 3, 6, 2, 7, 1, 5, 8, 9],
    [1, 8, 2, 3, 9, 5, 7, 6, 4],
    [5, 9, 7, 8, 4, 6, 3, 2, 1],
    [9, 1, 5, 6, 8, 4, 2, 7, 3],
    [7, 4, 8, 5, 3, 2, 1, 9, 6],
    [6, 2, 3, 9, 1, 7, 4, 5, 8],
    [2, 7, 4, 1, 6, 9, 8, 3, 5],
    [3, 5, 9, 4, 2, 8, 6, 1, 7],
    [8, 6, 1, 7, 5, 3, 9, 4, 2]])




start = time()

end = time()
print(end - start)

@njit(fastmath = True)
def turn(lst):
   lst_turn=lst.transpose()
   return lst_turn

@njit(fastmath = True)
def chek(lst):
   for y in lst:
      if len(np.array([i for i in y if i!=0]))<9:
         return False
   else:
      return True

print(chek(lst))