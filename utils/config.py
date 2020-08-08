import time
import random

INPUT_DIR = './dataset/'
OUTPUT_DIR = './output/'
ITERS = 5
CPU_PROCESSES = 20

HASH_BASE = 10**9 + 7


def getSeed(a=None):
    # return 69
    if a != None:
        return a % HASH_BASE
    return int(time.time() * 10**8) % HASH_BASE


APPLY_FLIP = True

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

APPLY_CUT = True
CUT_WIDTH_MIN = 0.5
CUT_WIDTH_MAX = 1.0
CUT_HEIGHT_MIN = 0.5
CUT_HEIGHT_MAX = 1.0
# Threshold used to determine if a bbox should be eliminated
# More precisely, bbox will be removed if the following condition is satisfied:
# intersection(bbox, new_img).area < CUT_ELIMINATE_THRESHOLD * bbox.area
CUT_ELIMINATE_THRESHOLD = 0.5

APPLY_SHARPEN = True