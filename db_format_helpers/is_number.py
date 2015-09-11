__author__ = 'thorsteinn'

def is_number(s):
    try:
        float(s)
        return True
    except ValueError, me:
        if len(s.replace(',', '')) < len(s):
            return is_number(s.replace(',', ''))
        return False
    except TypeError, me:
        return False
    except AttributeError, me:
        return False


if __name__ == '__main__':
    is_number(s)