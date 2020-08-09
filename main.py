import os
import cv2
import time
import copy
import json
import random as rd
from multiprocessing import Pool, Manager
from itertools import repeat
from utils.config import *
from utils.img_proc import *
from utils.json_utils import *
import numpy as np


def copyCOCO(annotation):
    annotation_new = copy.deepcopy(annotation)
    annotation_new['images'] = []
    annotation_new['annotations'] = []
    return copy.deepcopy(annotation_new)


def genNewAnnotation(annotation_list, annotation):
    annotation_new = copyCOCO(annotation)
    for ann in annotation_list:
        annotation_new['images'] += ann['images']
        annotation_new['annotations'] += ann['annotations']
    return annotation_new


def augmentImage_core(fi, annotation, annotation_new, seed, image_id):
    rd.seed(seed)
    img_path = os.path.join(INPUT_DIR, fi)
    out_img_name = os.path.splitext(fi)[0] + '_' + str(seed) + '.jpg'
    initJsonImage(annotation_new, out_img_name, image_id)
    
    img = cv2.imread(img_path)
    
    if APPLY_FLIP and rd.randrange(2):
        img = img[:,::-1,:]
        flipJsonImage(annotation_new)
        
    if APPLY_CUT and rd.randrange(2):
        img, top_left, bottom_right = applyCut(img)
        cutJsonImage(annotation_new, top_left, bottom_right)

    if APPLY_SHADE:
        use_gamma = rd.randrange(2)
        img = applyDarkShade(img, use_gamma)
        
    if APPLY_HSV:
        img = applyHSV(img)
        
    if APPLY_SHARPEN and rd.randrange(2):
        img = applySharpen(img)

    out_img_path = os.path.join(OUTPUT_DIR, out_img_name)
    cv2.imwrite(out_img_path, img)
    return annotation_new


def augmentImage(fi, annotation, seed, image_id):
    image_id = int(image_id)
    annotation_list = []
    annotation_new = copyCOCO(annotation)
    createJsonTemplate(annotation_new, annotation, fi)
    for i in range(ITERS):
        annotation_list.append(augmentImage_core(
            fi, annotation, copy.deepcopy(annotation_new), getSeed(seed + i), image_id * ITERS + i))

    return genNewAnnotation(annotation_list, annotation)


def augmentDir(dir, annotation):
    manager = Manager()
    tmp_annotation = manager.dict(annotation)
    pool = Pool(processes=CPU_PROCESSES)
    seed = getSeed()
    image_id = np.array(range(len(dir)))
    annotation_list = pool.starmap(
        augmentImage, zip(dir, repeat(tmp_annotation), repeat(seed), image_id,))

    return genNewAnnotation(annotation_list, annotation)


def main():
    with open(os.path.join(INPUT_DIR, 'labels.json'), 'r') as fi:
        annotation = json.load(fi)

    dir = os.listdir(INPUT_DIR)
    dir = [fi for fi in dir if os.path.splitext(
        fi)[1] in ['.jpg', '.png']]  # Takes only image files
    dir.sort()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    annotation_res = augmentDir(dir[:], annotation)
    annotation_path = os.path.join(OUTPUT_DIR, 'labels.json')
    with open(annotation_path, 'w') as fo:
        json.dump(annotation_res, fo, indent=2)


if __name__ == '__main__':
    t = time.time()
    main()
    print(str(int(time.time()-t)) + " seconds elapsed.")
