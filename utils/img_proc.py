import numpy as np
import random as rd
from utils.config import *

def applyDarkShade(img, use_gamma=True):
    height, width = img.shape[:2]
    x = rd.randint(int(height * SHADE_RANGE[0]), int(height * SHADE_RANGE[1]))
    y = rd.randint(int(width * SHADE_RANGE[0]), int(width * SHADE_RANGE[1]))
    h = int(height * SHADE_SIZE)
    w = int(width * SHADE_SIZE)

    img_new = img.astype(np.float) / 255.0
    shade = img_new[x:x+h, y:y+w, :].copy()

    if use_gamma:
        gamma = rd.uniform(SHADE_GAMMA_MIN, SHADE_GAMMA_MAX)
        gamma = np.full_like(shade, gamma)
        shade = np.power(shade, gamma)
    else:
        shade_shift = rd.uniform(SHADE_SHIFT_MIN, SHADE_SHIFT_MAX)
        shade -= shade_shift

    img_new[x:x+h, y:y+w, :] = shade
    img_new = np.clip(img_new, 0, 1) * 255
    return img_new.astype(np.uint8)