__author__ = 'thorsteinn'


def is_int(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    except TypeError:
        return False
    except AttributeError:
        return False
    else:
        return a == b