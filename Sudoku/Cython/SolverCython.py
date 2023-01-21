from SaveGetTxt import *
from Timer import timer
import isprime


def show(lst):
    for row in lst:
        for cell in row:
            print(cell, end='  ')
        print()
    print()


@timer
def run(lst):
    show(lst)

    Solver = isprime.Solver(sud)
    res = Solver.run()

    show(res)


@timer
def run_random(lst):
    show(lst)

    Solver = isprime.Solver(sud)
    res = Solver.solver_random()

    show(res)


@timer
def run_all_solver(lst):
    show(lst)

    Solver = isprime.Solver(sud)
    solvers = Solver.run_all_variant()

    print(f'Всего решений {len(solvers)}')
    show(solvers[0])
    print('_' * 25)


if __name__ == '__main__':
    sud, sol = get_sudoku(20, 1)

    # run(sud)
    # run_random(sud)
    # run_all_solver(sud)