def assert_(value, message=None):
    if message is None:
        assert value
    else:
        assert value, message

def raise_(error):
    raise error

def value_or(func, fallback):
    try:
        return func()
    except:
        return fallback