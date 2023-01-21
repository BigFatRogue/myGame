import time


def timer(func):
    def wrapper(*args):
        start = time.time()
        res = func(*args)
        end = time.time()
        print(f'Время выполнения: {end - start:0.04}', 'сек')
        return res
    return wrapper