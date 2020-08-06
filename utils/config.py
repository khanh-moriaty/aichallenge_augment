import time
import random

INPUT_DIR = './dataset/'
OUTPUT_DIR = './output/'
ITERS = 5
CPU_PROCESSES = 5

HASH_BASE = 10**9 + 7
def getSeed(a = None):
    # return 69
    if a != None: return a % HASH_BASE
    return int(time.time() * 10**8) % HASH_BASE

APPLY_SHADE = True
SHADE_RANGE = (0, .5)
SHADE_SIZE = 0.6
SHADE_SHIFT_MIN = -0.15
SHADE_SHIFT_MAX = +0.15
SHADE_GAMMA_MIN = .75
SHADE_GAMMA_MAX = 2

APPLY_HSV = True
HUE_MIN = -0.05
HUE_MAX = +0.05
SATURATION_MIN = -0.15
SATURATION_MAX = +0.15
HSV_VALUE_MIN = -0.15
HSV_VALUE_MAX = +0.15