from types import FunctionType

DefaultArg = object()


def callable(f):
    return hasattr(f, "__call__") or isinstance(f, FunctionType)


def iterable(x):
    try:
        _ = (i for i in x)
    except TypeError:
        return False
    return True
