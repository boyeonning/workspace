from glob import glob
import xml.etree.ElementTree as ET

class Changelabel:
    def __init__(self, xml_path):
        self.xml_path = xml_path

    def is_inside(self, bbox1, bbox2):
        """
        Check if the center of bbox1 is inside bbox2.
        Args:
            bbox1: Tuple or List representing (x1, y1, x2, y2) coordinates of bounding box 1.
            bbox2: Tuple or List representing (x1, y1, x2, y2) coordinates of bounding box 2.
        Returns:
            Boolean value indicating whether bbox1 is inside bbox2 or not.
        """
        x1, y1, x2, y2 = bbox1
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        x1, y1, x2, y2 = bbox2
        return x1 < center_x < x2 and y1 < center_y < y2

    def parse_annotation(self):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        
        objects = []
        for obj in root.findall('object'):
            obj_info = {}
            obj_info['name'] = obj.find('name').text
            obj_info['pose'] = obj.find('pose').text
            obj_info['truncated'] = int(obj.find('truncated').text)
            obj_info['difficult'] = int(obj.find('difficult').text)
            bbox = obj.find('bndbox')
            obj_info['xmin'] = int(bbox.find('xmin').text)
            obj_info['ymin'] = int(bbox.find('ymin').text)
            obj_info['xmax'] = int(bbox.find('xmax').text)
            obj_info['ymax'] = int(bbox.find('ymax').text)
            objects.append(obj_info)
        
        return objects

    def modify_object_name(self, object_index, new_name):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        
        objects = root.findall('object')
        if object_index < len(objects):
            objects[object_index].find('name').text = new_name
            tree.write(xml_file)
            print(f"Object name at index {object_index} has been modified to '{new_name}'.")
        else:
            print("Invalid object index.")

    def remove_object_by_index(self, object_index):
        """
        Remove object from XML file based on object index.

        Args:
            xml_file (str): Path to the XML file.
            object_index (int): Index of the object to be removed.

        Returns:
            bool: True if object is removed successfully, False otherwise.
        """
        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()

            objects = root.findall('object')
            if object_index < len(objects):
                obj_to_remove = objects[object_index]
                root.remove(obj_to_remove)
                tree.write(self.xml_path)
                print(f"Object at index {object_index} removed successfully.")
                return True
            else:
                print("Invalid object index.")
                return False

        except Exception as e:
            print("Error:", e)
            return False


if __name__ == "__main__":
    xml_dir = '/home/boyeon/Desktop/data/xml'
    xml_psth_list = glob(xml_dir + '/*.xml')
    
    for xml_file in xml_psth_list:
        change_obj = Changelabel(xml_file)

# XML 파일 파싱하여 객체 정보 추출
        objects = change_obj.parse_annotation()

    # 개별 객체 정보 출력
        dic={'large':{}, 'small':{}}
        for i, obj in enumerate(objects):
            name = obj['name']
            if name != 'object':
                if name not in dic['large']:
                    dic['large'][name] = []
                dic['large'][name].append((obj['xmin'], obj['ymin'], obj['xmax'], obj['ymax']))
            else:
                dic['small'][i]=[]
                dic['small'][i].append((obj['xmin'], obj['ymin'], obj['xmax'], obj['ymax']))
            # print(dic)

        for label,box1 in dic['large'].items():
            for b in box1:
                for idx,box2 in dic['small'].items():
                    if change_obj.is_inside(box2[0], b):
                        change_obj.modify_object_name(idx, label)

    # for label,box1 in dic['large'].items():
    #     remove_idx = label.split('_')[-1]
    #     change_obj.remove_object_by_index(xml_file, remove_idx)