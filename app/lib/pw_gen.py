###############################################
# Simple module to generate a random password #
###############################################

import string
import random

def pw_gen(size=8, chars=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))