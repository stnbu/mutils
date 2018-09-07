# -*- mode: python; coding: utf-8 -*-

import functools

def memoized(f):
    """Decorate a function (without arguments), caching its results and returning the cache when available.
    """
    proxy_name = '_' + f.__name__
    @functools.wraps(f)
    def wrapper(self):
        if hasattr(self, proxy_name):
            return getattr(self, proxy_name)
        setattr(self, proxy_name, f(self))
        return getattr(self, proxy_name)
    return wrapper
