import cv2
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


def applyHSV(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    img_hsv = img_hsv.astype(np.float) / 255.0
    img_hsv[:, :, 0] += rd.uniform(HUE_MIN, HUE_MAX)
    img_hsv[:, :, 1] += rd.uniform(SATURATION_MIN, SATURATION_MAX)
    img_hsv[:, :, 2] += rd.uniform(HSV_VALUE_MIN, HSV_VALUE_MAX)
    img_hsv = np.clip(img_hsv, 0, 1) * 255

    img = cv2.cvtColor(img_hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    return img


def applyCut(img):
    height, width = img.shape[:2]
    new_width = int(width * rd.uniform(CUT_WIDTH_MIN, CUT_WIDTH_MAX))
    new_height = int(height * rd.uniform(CUT_HEIGHT_MIN, CUT_HEIGHT_MAX))
    xmin = rd.randrange(width - new_width + 1)
    ymin = rd.randrange(height - new_height + 1)
    xmax = xmin+new_width-1
    ymax = ymin+new_height-1
    img_new = img[ymin:ymax+1, xmin:xmax+1]
    return img_new, (xmin, ymin), (xmax, ymax)

def applySharpen(img):
    kernel = np.array([[-0.0,-1.0,-0.0], [-1.0,4.0,-1.0], [-0.0,-1.0,-0.0]], dtype=np.float)
    kernel = kernel / 6
    kernel[1,1] += 1.0
    img_new = cv2.filter2D(img, -1, kernel)
    return img_new
