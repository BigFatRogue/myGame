import inspect


def func():
    return 2


print(inspect.getsource(func))