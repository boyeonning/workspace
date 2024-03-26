import os
import glob
import pymssql
import pandas as pd
import xml.etree.ElementTree as ET

from get_db import GetDB
from datetime import datetime
from distutils.dir_util import copy_tree

class AnnotationProcessor:
    def __init__(self, xml_dir):
        self.xml_dir = xml_dir # both dir path and file path

    def parse_annotation(self):
        """
        Parse XML annotation files and return a DataFrame.
        다른 format 형식으로 라벨링 할 경우 그 format에 맞게 parsing해서 사용해야함.
        """
        dic = {}
        if os.path.isdir(self.xml_dir):
            xml_list = glob.glob(self.xml_dir + '/*.xml')
        else:
            xml_list = [self.xml_dir]

        for xml in xml_list:
            tree = ET.parse(xml)
            root = tree.getroot()
            for x in root.findall('object'):
                name = (x.find('name').text)
                if name not in dic:
                    dic[name]=0
                dic[name]+=1

        sku_id = dic.keys() 
        patch_count= dic.values()
        df = pd.DataFrame({'sku_id': sku_id, 'patch_count':patch_count}).sort_values(by='patch_count', ascending=False)
        df['sku_id'] = df['sku_id'].astype(int)
        return df

class SKUProcessor:
    def __init__(self):
        self.server = '192.168.0.85:11433'
        self.user = 'interminds'
        self.password = 'ntflow'
        self.database = 'cspace_test'
        self.port = 11433
        self.conn = pymssql.connect(self.server, self.user, self.password, self.database, charset='CP949')

    def fetch_sku_train(self):
        """
        Fetch SKU training data from database and return as DataFrame.
        """
        sql = """
            SELECT * from sku_train st ;
             """
        cursor = self.conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        columns=['sku_id','product_name','manufacturer','ref_image_file','used_for_tr','sku_barcode','category','class_info_id','barcode','excel_no','brand_nm']
        self.conn.close()
        return pd.DataFrame(records, columns=columns)

def merge_annotation_and_sku_data(annotation_df, sku_train_df):
    """
    Merge annotation DataFrame with SKU training DataFrame based on 'excel_no' column.
    Args:
        annotation_df (pd.DataFrame): DataFrame containing annotation data.
        sku_train_df (pd.DataFrame): DataFrame containing SKU training data.
    Returns:
        pd.DataFrame: Merged DataFrame containing SKU information along with annotation data.
    """
    merged_df = annotation_df.merge(sku_train_df, left_on = 'sku_id', right_on = 'sku_id')
    merged_df = merged_df[['sku_id', 'patch_count', 'product_name', 'manufacturer', 'category', 'brand_nm', 'barcode']]
    return merged_df

def change_label_names_in_xml_files(xml_dir, old_label=None, new_label=None):
    """
    Change label names in XML annotation files.
    """
    old_label, new_label = str(old_label), str(new_label)
    xml_list = glob.glob(xml_dir + '/*.xml')
    for xml_file in xml_list:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        for x in root.iter('name'):
            name = x.text
            if name == old_label:
                x.text = name.replace(old_label, new_label)
        tree.write(xml_file)

def update_label_under_limit(merged_df, threshold):
    """
    Update labels with patch count under the threshold
    patch개수가 n개 미만인 라벨을 "manufacturer_brand_nm_기타" 로 묶기 위한 작업
    """
    for i in range(len(merged_df)):
        if merged_df.loc[i, 'patch_count'] < threshold:
            # merged_df.loc[i, 'new_name'] = str(merged_df.loc[i, 'brand_nm']) + '_기타'
            merged_df.loc[i, 'modified_product_name'] = str(merged_df.loc[i, 'manufacturer']) + ' ' + str(merged_df.loc[i, 'brand_nm']) + ' 기타'
        else:
            pass

    # modified_labels = [(f'etc_{i-1}', v) for i, v in enumerate(merged_df['modified_product_name'].unique()) if type(v) != float]
    # a = [i[0] for i in modified_labels]
    # b = [i[1] for i in modified_labels]
    # etc_df = pd.DataFrame({'modified_excel_no':a, 'modified_product_name':b})
    unique_modified_labels = merged_df['modified_product_name'].unique()
    modified_labels_df = pd.DataFrame({'modified_sku_id':[f'etc_{i-1}' for i in range(len(unique_modified_labels)) if type(unique_modified_labels[i]) != float], 
                                       'modified_product_name' :[i for i in unique_modified_labels if type(i) != float]})
    df = pd.merge(merged_df, modified_labels_df, how='left', on='modified_product_name')
    return df

def make_class_info(file_name, sheet_name, df):
    writer=pd.ExcelWriter(file_name, engine='openpyxl')
    df[0].to_excel(writer, sheet_name=sheet_name[0])
    df[1].to_excel(writer, sheet_name=sheet_name[1])
    writer.save()

if __name__ == '__main__' :
    xml_dir = '/home/boyeon/Desktop/workspace/code/annotation_program/xml_test'
    annotation_processor = AnnotationProcessor(xml_dir)
    annotation_df = annotation_processor.parse_annotation()

    sku_processor = SKUProcessor()
    sku_train_df = sku_processor.fetch_sku_train()

    merged_df = merge_annotation_and_sku_data(annotation_df, sku_train_df)
    df = update_label_under_limit(merged_df, 30)
    df.loc[df['modified_sku_id'].notna(),'barcode']= '' # etc로 바꾼 행 바코드 None값으로 

    for i in range(len(df)):
        if type(df.loc[i, 'modified_sku_id']) == float:
            df.loc[i, 'modified_sku_id'] =  df.loc[i, 'sku_id']

        if type(df.loc[i, 'modified_product_name']) == float:
            df.loc[i, 'modified_product_name'] = df.loc[i, 'product_name']

    temp = df.groupby(by='modified_sku_id')['patch_count'].sum().reset_index()
    # print(temp.sort_values(by='patch_count', ascending=False))

    temp_label = set(temp[temp['patch_count']<15]['modified_sku_id'].to_list())
    
    for i in range(len(df)):
        if df.loc[i, 'modified_sku_id'] in temp_label:
            df.loc[i, 'modified_sku_id'] = 'etc'
  
    label_info = df[['sku_id', 'modified_sku_id']]
    label_info.columns = ['sku_id in sku_train','sku_id in class_info']
    # make_class_info('class_infov1.xlsx', 'label_info', label_info)
    
    df.drop_duplicates('modified_sku_id', inplace=True)
    df.drop(labels=['sku_id','patch_count','product_name'], axis=1, inplace=True)
    df.rename(columns={'modified_sku_id':'sku_id', 'modified_product_name':'product_name'}, inplace=True)
    df = df[['sku_id','barcode','product_name','manufacturer','category','brand_nm']].reset_index()
    df.drop(labels='index', axis=1, inplace=True)

    df.loc[df['sku_id']=='etc', ['barcode','manufacturer','category','brand_nm']] = ''
    df.loc[df['sku_id']=='etc', 'product_name'] = '기타'
    make_class_info('class_info_v3.xlsx', ['class_info', 'label'], [df, label_info])






# # 라벨 인포 시트 부분 보고 라벨 바꾸는 부분
#     추후에 라벨 바꿀 경우 시트에 적고 하셈

    ch = pd.read_excel('class_info_v3.xlsx', sheet_name='label')
    
    today = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    copy_xml_path = f'{today}_xml'
    xml_copy = copy_tree(annotation_processor.xml_dir, copy_xml_path)

    # class info를 먼저 만들고 저장하고 xml 변경 
    for idx, v in ch.iterrows():
        before = v['sku_id in sku_train']
        after = v['sku_id in class_info']
        if before != after: 
            print(v['sku_id in sku_train'], v['sku_id in class_info'])
            change_label_names_in_xml_files(copy_xml_path, before, after)

    

