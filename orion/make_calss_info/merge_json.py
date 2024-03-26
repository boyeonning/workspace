import os
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from glob import glob
import pandas as pd

def load_json(json_path):
    '''
    Load the json file   
    Args:
        json_path : json path
    '''
    with open(json_path,'r') as json_file:
        anno_json = json.load(json_file)
    return anno_json


def save_json(unified_json, unified_json_path):
    '''
    Save the finalized annotation file

    Args:
        unified_json: The finalized JSON file
        unified_json_path: The path to save the finalized json file
    '''
    os.makedirs(Path(unified_json_path).parent, exist_ok=True)
    with open(unified_json_path, 'w') as json_file:
        json.dump(unified_json, json_file)


def save_binary_json(unified_json, unified_binary_json_path ):
    '''
    Save the binary binary annotation file

    Args:
        unified_json: The finalized JSON file
        unified_binary_json_path : The path to save the finalized json file
    '''
    anno = unified_json

    anno['categories'] = [{'id': 0, 'name': 'Product'}]
    for i in anno['annotations']:
        i['category_id'] = 0
        
    with open(Path(unified_binary_json_path),'w') as json_file:
        json.dump(anno, json_file)


def main(base_path):
    add_json_path = Path(f'{base_path}/annotations/annotation.json')
    add_excel_path = Path(glob(f'{base_path}/annotations/*.xlsx')[-1])

    # Error check
    if not os.path.isfile(add_json_path) or not os.path.isfile(add_excel_path):
        raise "File Not Exist"
    
    add_json = load_json(add_json_path)
    add_excel = pd.read_excel(add_excel_path, index_col=0)

    if not (add_excel.columns == ['id', 'name', 'manufacturer']).all():
        raise "Excel content is different"
    
    try:
        add_json['images']
        add_json['categories']
        add_json['annotations']
    except:
        raise "Json content is different"

    if len(add_json['categories']) != len(add_excel):
        raise "Excel and Json number is different"

    # add json train_valid split
    add_train_images, add_valid_images = train_test_split(add_json['images'], test_size=0.2, random_state=42)

    # 정돈
    add_train_images.sort(key=lambda x : x['id'])
    add_valid_images.sort(key=lambda x : x['id'])

    add_train_json = {'images' : add_train_images, 'categories' : add_json['categories'], 'annotations' : []}
    add_valid_json = {'images' : add_valid_images, 'categories' : add_json['categories'], 'annotations' : []}

    target_id = [i['id'] for i in add_train_images]
    for anno in add_json['annotations']:
        if anno['image_id'] in target_id:
            add_train_json['annotations'].append(anno)
        else:
            add_valid_json['annotations'].append(anno)

    # save
    save_json(add_train_json, Path(f'{base_path}/annotations/annotation_train.json'))
    save_json(add_valid_json, Path(f'{base_path}/annotations/annotation_valid.json'))

    # save binary
    save_binary_json(add_train_json, Path(f'{base_path}/annotations/annotation_binary_train.json'))
    save_binary_json(add_valid_json, Path(f'{base_path}/annotations/annotation_binary_valid.json'))


if __name__ == "__main__":
    base_path = './add/'

    main(base_path)