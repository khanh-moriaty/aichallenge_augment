import time
import random

INPUT_DIR = './dataset/'
OUTPUT_DIR = './output/'
CPU_PROCESSES = 1
ITERS = 1

def getSeed():
    return 69

SHADE_RANGE = (0, .5)
SHADE_SIZE = 0.6
SHADE_SHIFT_MIN = -0.05
SHADE_SHIFT_MAX = +0.15
SHADE_GAMMA_MIN = .75
SHADE_GAMMA_MAX = 2