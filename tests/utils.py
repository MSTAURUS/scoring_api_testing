#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                try:
                    f(*new_args)
                except Exception:
                    raise ValueError("Fail in {} case.".format(c)) #new_args[1]

        return wrapper

    return decorator
