import os
import time
import urllib
import requests
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup as bs


def get_img(dst, barcode, barname):
    url = f'https://www.beepscan.com/barcode/{barcode}'
    resp = requests.get(url)
    soup = bs(resp.content, 'lxml')
    if soup.find('img') != None and soup.find('img')['src'] != '':
        img_src = soup.find('img')['src']
        print(dst)
        urllib.request.urlretrieve(img_src, f'{dst}/{barname}_{barcode}.jpg')
    else:
        print('X', barname, barcode)
        with open (os.path.join(dst,'not_exist.txt'), 'a') as f:
            f.write(str(barname) + ' ' + str(barcode) + '\n')
    return barcode, barname
   

if __name__ == '__main__':
    root = 'orion_class'

    path = 'sku.csv'
    df = pd.read_csv(path)
    df.dropna(subset=['brandnm'], inplace=True)
    dic = {}
    for i, v in df.iterrows():
        categorynm = v['categorynm']
        if categorynm in ('파이', '스낵', '비스켓'):
            brandnm = v['brandnm']
            barname = v['barname']
            barcode = v['barcode']
            if categorynm not in dic:
                dic[categorynm] = {}
            if brandnm not in dic[categorynm]:
                dic[categorynm][brandnm] = []
            dic[categorynm][brandnm].append((barname, barcode))

    root = 'orion_class'
    for categorynm, v in dic.items():
        for brandnm,v in v.items():
            dst = os.path.join(root, categorynm, brandnm)
            os.makedirs(dst, exist_ok=True)
            for x in v:
                barname = x[0]
                barcode = x[1]
                print(get_img(dst, barcode, barname))
                time.sleep(1)


# dic = {'test':[]}
# num = 0
# for barcode in test:
#     url = f'https://www.beepscan.com/barcode/{barcode}'
#     resp = requests.get(url)
#     soup = bs(resp.content, 'lxml')
#     # print(type(soup.find('img')['src']))
#     if soup.find('img') != None and soup.find('img')['src'] != '':
#         img_src = soup.find('img')['src']
#         urllib.request.urlretrieve(img_src, f'{num}_{barcode}.jpg')
#     else:
#         dic['test'].append(barcode)
#     num+=1


# print(dic))