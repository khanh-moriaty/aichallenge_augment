import copy
    
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

def initJsonImage(annotation_new, annotation, out_img_name, fi):
    out_img_id = hash(out_img_name) % (10**9 + 7)

    out_img_jsimg = copy.deepcopy(findJsImg(annotation, fi))
    img_id = out_img_jsimg['id']
    out_img_obj_list = copy.deepcopy(findJsAnn(annotation, img_id))
    out_img_jsimg['file_name'] = out_img_name
    out_img_jsimg['id'] = out_img_id
    for obj in out_img_obj_list:
        obj['id'] = (obj['id'] * obj['image_id'] +
                     out_img_id) % (10**9 + 7)
        obj['image_id'] = out_img_id

    annotation_new['annotations'] += out_img_obj_list
    annotation_new['images'].append(out_img_jsimg)
    
def flipJsonImage(annotation_new):
    width = annotation_new['images'][0]['width']
    height = annotation_new['images'][0]['height']
    obj_list = annotation_new['annotations']
    for obj in obj_list:
        obj['bbox'][0] = width - obj['bbox'][0]
        obj['bbox'][1] = height - obj['bbox'][1]
        
def cutJsonImage(annotation_new, top_left, bottom_right):
    pass