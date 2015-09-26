from make_pdf import make_pdf
import random

def rand_string(): # returns nice 6 character strings
    to_return = ""
    i = 0
    while i < 15:
        if random.randint(0,1): # If we get a 1, we do letters
            to_return += chr(random.randint(97,122))
        else: # we get a 0, we do a number
            to_return += str(random.randint(1,9))
        i += 1
    return to_return

