import copy
import json
from shapely.geometry import Polygon
from utils.config import CUT_ELIMINATE_THRESHOLD, OBJ_PER_IMG, HASH_BASE


def findJsImg(annotation, img_file):
    annotation = annotation['images']
    for img in annotation:
        if img['file_name'] == img_file:
            return img

    return None


def findJsAnn(annotation, img_id):
    annotation = annotation['annotations']
    obj_list = []
    for obj in annotation:
        if obj['image_id'] == img_id:
            obj_list.append(obj)

    return obj_list

def createJsonTemplate(annotation_new, annotation, fi):
    out_img_jsimg = copy.deepcopy(findJsImg(annotation, fi))
    img_id = out_img_jsimg['id']
    out_img_obj_list = copy.deepcopy(findJsAnn(annotation, img_id))

    annotation_new['annotations'] += out_img_obj_list
    annotation_new['images'].append(out_img_jsimg)
    
def initJsonImage(annotation_new, out_img_name, image_id):
    out_img_id = hash(out_img_name) % (10**9 + 7)
    out_img_id = image_id * OBJ_PER_IMG
    
    out_img_jsimg = annotation_new['images'][0]
    out_img_jsimg['file_name'] = out_img_name
    out_img_jsimg['id'] = out_img_id
    
    out_img_obj_list = annotation_new['annotations']
    for index, obj in enumerate(out_img_obj_list):
        obj['id'] = out_img_id + index + 1
        obj['image_id'] = out_img_id


def flipJsonImage(annotation_new):
    width = annotation_new['images'][0]['width']
    height = annotation_new['images'][0]['height']
    obj_list = annotation_new['annotations']
    for obj in obj_list:
        obj['bbox'][0] = width - obj['bbox'][0]
        obj['bbox'][1] = height - obj['bbox'][1]


def cutJsonImage(annotation_new, top_left, bottom_right):
    width = annotation_new['images'][0]['width']
    height = annotation_new['images'][0]['height']
    xmin, ymin = top_left
    xmax, ymax = bottom_right
    
    annotation_new['images'][0]['width'] = xmax - xmin + 1
    annotation_new['images'][0]['height'] = ymax - ymin + 1
    
    # large_img = Polygon(
    #     [(0, 0), (width-1, 0), (width-1, height-1), (0, height-1)])
    small_img = Polygon([(xmin, ymin), (xmax, ymin),
                         (xmax, ymax), (xmin, ymax)])

    obj_list = annotation_new['annotations']
    for obj in obj_list[:]:
        obj_xmin = obj['bbox'][0]
        obj_ymin = obj['bbox'][1]
        obj_xmax = obj_xmin + obj['bbox'][2] - 1
        obj_ymax = obj_ymin + obj['bbox'][3] - 1
        obj_poly = Polygon([(obj_xmin, obj_ymin), (obj_xmax, obj_ymin),
                            (obj_xmax, obj_ymax), (obj_xmin, obj_ymax)])
        intersection = small_img.intersection(obj_poly)
        # Eliminate bboxes under certain threshold
        if intersection.area < CUT_ELIMINATE_THRESHOLD * obj_poly.area:
            obj_list.remove(obj)
            continue

        if obj_xmin < xmin:
            obj_xmin = xmin
        if obj_ymin < ymin:
            obj_ymin = ymin
        if obj_xmax > xmax:
            obj_xmax = xmax
        if obj_ymax > ymax:
            obj_ymax = ymax
            
        obj['bbox'][0] = obj_xmin - xmin
        obj['bbox'][1] = obj_ymin - ymin
        obj['bbox'][2] = obj_xmax - obj_xmin + 1
        obj['bbox'][3] = obj_ymax - obj_ymin + 1
