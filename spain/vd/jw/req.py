import cv2
import json
import base64
import urllib3
import requests
import numpy as np
import multiprocessing as mp
import time

def encode(img: np.ndarray) -> str:
    img = cv2.resize(img, (224, 224))  # if product101(fridge & classification)
    img = img[:, :, ::-1]  # bgr to rgb
    img = cv2.imencode('.jpg', img)[1].tobytes()  # .png or .jpg
    img = base64.b64encode(img).decode('utf-8')
    return img


# api_url = 'https://192.168.0.113:8080/inference'
# api_key = 'pTsHkPdCyeFDolBRywQTcXurdbxBL7K2kstMoTHs'
# api_ids = 'VD'
 # --- 요청 데이터 ---


images = cv2.imread('/home/vd/vd/jw/asi.jpg')
# print(images)
images = encode(img = images)

payload = {
    'images': [images] * 48,
    'params': {},
}

# api_url = ['https://112.175.148.147:58123', 'https://112.175.148.147:58124']
api_url = 'http://112.175.148.147:52111/fr-cls-jw_test'
# api_url = 'http://172.18.0.9:8080/fr-cls-guinness_440'


resp = requests.post(
        url= api_url,   #돌리신 서버 주소:port/endpoint(fr-cls-cass_fresh...),
        data=json.dumps(payload),
        headers={
            "USER-ID": 'VD'
        },
        verify=False
    )
start = time.time()


result = resp.json()
print(result)