def is_evaluable(s):
    try:
        eval(s)
        return True
    except:
        return False
