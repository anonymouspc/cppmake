def value_or(func, fallback):
    try:
        return func()
    except:
        return fallback