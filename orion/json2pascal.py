import os
import json
import cv2
import shutil
from glob import glob
from pascal_voc_writer import Writer

json_path = 'sample_image/json'
img_dir_path = 'sample_image'
path_list = glob(json_path + '/*.json')

# font=cv2.FONT_HERSHEY_SIMPLEX
# for path in path_list:
#     with open(path, 'r') as f:
#         data = json.load(f)
#     file_name = data['image_info']['filename']
#     objects = data['objects']
#     img_path = os.path.join(img_dir_path, file_name)
#     img = cv2.imread(img_path)
#     w,h,_ = img.shape
#     # img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
#     for obj in objects:
#         bbox = obj['bbox']
#         # name = obj['name']
#         name = ''
#         confidence = round(obj['confidence'],2)
#         x, y, x2, y2 = bbox

#         if confidence < 0.3:
#             # test = cv2.rectangle(img, (int(x),int(y)), (int(x2), int((y2)) ), (0,0,255), 2)
#             pass
#         else:   
#             org = (int(x2-x)//2, int(y2-y)//2)
#             test = cv2.rectangle(img, (int(x),int(y)), (int(x2), int((y2)) ), (0,255,0), 2)
#     cv2.putText(img, 'confidence : 0.3', (100,10), font, 3, (0,255,255), 3)
#     cv2.imwrite(f'dataset/rst_image/{file_name}.jpg', test)


def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)  
    return data

def json2xml(path:str):
    data = load_json(path)

    file_name = data['image_info']['filename']
    image_height = data['image_info']['image_height']
    image_width = data['image_info']['image_width']
    xml_name = file_name.split('.jpg')[0] + '.xml'
    objects = data['objects']
    writer = Writer(file_name, image_width, image_height)
    for obj in objects:
        bbox = obj['bbox']
        bbox = [bbox[0], bbox[1], bbox[2], bbox[3]]
        bbox = [int(b) for b in bbox]
        name = 'object'
        conf = obj['confidence']
        if conf > 0.3:
            writer.addObject(name, bbox[0], bbox[1], bbox[2], bbox[3])
            writer.save(json_path + '/'+ xml_name)

if __name__ == '__main__':
    # for path in path_list:
        # json2xml(path)
