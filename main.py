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
from utils.json_utils import initJsonImage
import numpy as np

def copyCOCO(annotation):
    annotation_new = copy.deepcopy(annotation)
    annotation_new['images'] = []
    annotation_new['annotations'] = []
    return annotation_new

def augmentImage(fi, annotation, SEED):
    annotation_new = copyCOCO(annotation)
    img_path = os.path.join(INPUT_DIR, fi)
    out_img_name = os.path.splitext(fi)[0] + '_' + str(SEED) + '.jpg'
    initJsonImage(annotation_new, annotation, out_img_name, fi)

    img = cv2.imread(img_path)

    use_gamma = rd.randrange(2)
    img = applyDarkShade(img, use_gamma)

    out_img_path = os.path.join(OUTPUT_DIR, out_img_name)
    cv2.imwrite(out_img_path, img)
    return annotation_new

def augmentDir(dir, annotation):
    SEED = getSeed()
    annotation_new = copyCOCO(annotation)
    annotation_list = []
    for fi in dir:
        annotation_list.append(augmentImage(fi, annotation, SEED))
    for ann in annotation_list:
        annotation_new['images'] += ann['images']
        annotation_new['annotations'] += ann['annotations']
        
    return annotation_new

def main():
    with open(os.path.join(INPUT_DIR, 'labels.json'), 'r') as fi:
        annotation = json.load(fi)

    dir = os.listdir(INPUT_DIR)
    dir = [fi for fi in dir if os.path.splitext(fi)[1] in ['.jpg', '.png']] # Takes only image files
    dir.sort()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    annotation_res = copyCOCO(annotation)
    
    manager = Manager()
    pool = Pool(processes=CPU_PROCESSES)

    dir_list = [dir] * ITERS

    tmp_annotation = manager.dict(annotation)
    annotation_list = pool.starmap(augmentDir, zip(
        dir_list, repeat(tmp_annotation), ))

    # Merge result annotation from processes
    for ann in annotation_list:
        annotation_res['images'] += ann['images']
        annotation_res['annotations'] += ann['annotations']

    annotation_path = os.path.join(OUTPUT_DIR, 'labels.json')
    with open(annotation_path, 'w') as fo:
        json.dump(annotation_res, fo, indent=2)


if __name__ == '__main__':
    t = time.time()
    main()
    print(str(int(time.time()-t)) + " seconds elapsed.")
