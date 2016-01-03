# -*- coding: utf-8 -*-

"""Allows for creation of random strings"""

import random

def rand_string(length=15):
    """Returns randomly constructed strings of given `length`, default length
    15."""
    to_return = ""
    i = 0
    while i < length:
        if random.randint(0, 1): # If we get a 1, we do letters
            to_return += chr(random.randint(97, 122))
        else: # we get a 0, we do a number
            to_return += str(random.randint(1, 9))
        i += 1
    return to_return
