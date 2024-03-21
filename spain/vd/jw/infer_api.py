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

model_name = [
    'asahi_super_dry_500_can_tspn',
    'belgium_export_500',
    'belgium_pilsner_500',
    'belgium_weizen_500',
    'big_wave_golden_ale_473',
    'budweiser_500',
    'cass_fresh_355',
    'cass_fresh_500',
    'cass_light_500',
    'cass_zero_355',
    'edelweiss_500',
    'fil_good_500',
    'filite_fresh_500',
    'guinness_440',
    'hanmac_500',
    'heineken_500',
    'hoegaarden_500',
    'iseul_tok_tok_355',
    'jipyeong_makgeolli_750',
    'kgb_lemon_355',
    'kloud_500',
    'sanmiguel_pale_pilsen_500',
    'somersby_500',
    'soonhari_lemon_4_355',
    'soonhari_lemon_7_355',
    'stella_artois_500_can',
]

model_name = ['jw_test', 'cass_fresh_500']
# urls = [f'http://112.175.148.147:550{str(num+1).zfill(2)}/{model}' for num, model in enumerate(model_name_list)]

urls = 'http://112.175.148.147:58050/inference'

images = cv2.imread('./asi.jpg')
images = encode(img = images)

# --- 요청 데이터 ---
payload = {
    'images': [images] * 48,
    'device_type': 'fr',  # fr, cigar
    'model_type': 'cls',  # classification, detection
    'model_name': model_name,  # 00888_c_test, short_tall, cass, or [cass, terra], ...
    'master' : [f'a_{i}' for i in range(1,49)],
    'params': {
        'cm': 0,
    }
}
start = time.time()

# --- 요청 ---
response = requests.post(
    url = urls,
    data = json.dumps(payload),
    verify=False
)

result = response.json()
print(result)
# aaa = [f'a_{i}' for i in range(1,49)]
# print(aaa)
# {'main': {'images': [], 'device_type': 'fr', 
#     'model_type': 'cls', 
#     'model_name': ['jw_test', 'cass_fresh_500'], 
#     'master': ['terra_355', 'terra_355', 'terra_355', 
#         'terra_355', 'cass_fresh_355', 'cass_fresh_355', 
#         'cass_fresh_355', 'cass_fresh_355', 'terra_500', 
#         'terra_500', 'terra_500', 'terra_500', 'cass_fresh_500',
#          'cass_fresh_500', 'cass_fresh_500', 'cass_fresh_500', 
#          'kloud_500', 'kloud_500', 'kloud_500', 'kloud_500', 
#          'kloud_draft_500', 'kloud_draft_500', 'kloud_draft_500',
#           'kloud_draft_500', 'edelweiss_500', 'edelweiss_500', 
#           'edelweiss_500', 'edelweiss_500', 'heineken_500', 
#           'heineken_500', 'heineken_500', 'heineken_500',
#            'hoegaarden_500', 'hoegaarden_500', 'hoegaarden_500',
#             'hoegaarden_500', 'hanmac_500', 'hanmac_500', 
#             'hanmac_500', 'hanmac_500', 'guinness_440', 
#             'guinness_440', 'guinness_440', 'guinness_440', 
#             'guinness_440', 'guinness_440', 'guinness_440', 
#             'guinness_440'],
#     'params': {'cm': 0}}}

