#-*- coding: utf-8 -*-
'''
coding by JW_Mudfish
Version : 2.1 
Last Updated 2020.11.03
'''

import pandas as pd
import cv2
import numpy as np
import imutils
from datetime import datetime
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import random
import copy

# sudo apt install v4l-utils
###############################
BRIGHTNESS = 0
# save_dir = ''
save_dir = '/home/vision/Desktop/jiyoon/crop'


save_dir_pullimg = '/home/vision/Desktop/jiyoon/full'
save_dir_pullimg_l = '/home/vision/Desktop/jiyoon/full'
save_dir_pullimg_r = '/home/vision/Desktop/jiyoon/full'
# save_dir_pullimg = '/mnt/germany/short_tall_can'

LEFT_CAMERA_NUM = 2
RIGHT_CAMERA_NUM = 4

frame_width = int(1920)
frame_height = int(1080)

################################
os.makedirs(save_dir_pullimg, exist_ok=True)

MODE = 'b'   # b : box 모드
BOX_NUM_1 = '0'   # 
BOX_NUM_2 = '0'

def get_boxes(label_path):
    label_path = label_path
    xml_list = os.listdir(label_path)


    boxes_1 = {}
    cnt = 0
    for xml_file in sorted(xml_list):
        if xml_file =='.DS_Store':
            pass
        else:
                #try:
            xml_path = os.path.join(label_path,xml_file)

            root_1 = minidom.parse(xml_path)
            bnd_1 = root_1.getElementsByTagName('bndbox')

            result = []
            for i in range(len(bnd_1)):
                xmin = int(bnd_1[i].childNodes[1].childNodes[0].nodeValue)
                ymin = int(bnd_1[i].childNodes[3].childNodes[0].nodeValue)
                xmax = int(bnd_1[i].childNodes[5].childNodes[0].nodeValue)
                ymax = int(bnd_1[i].childNodes[7].childNodes[0].nodeValue)
                result.append((xmin,ymin,xmax,ymax))

            result.sort(key = lambda x:x[0])

            boxes_1[str(cnt)] = result
            cnt += 1
    
    return boxes_1

def make_folder(label_dir):
    if not os.path.exists(save_dir +'/' + label_dir):
        os.makedirs(save_dir +'/' + label_dir)

def get_labels(label_path):
    with open(f'{label_path}', 'r') as file:
        labels = file.readlines()
        labels = list(map(lambda x : x.strip(), labels))

    return labels

def get_multi_labels(label_path):
    with open(f'{label_path}', 'r') as file:
        labels = file.readlines()
        labels = list(map(lambda x : x.strip(), labels))
    
    left = labels[:int(np.ceil(len(labels) / 2))]
    right = labels[int(np.ceil(len(labels) / 2)) :]
    return left, right


def crop_random_image(image, boxes, save_path, labels, left_right, resize = None):
    seed_image = image

    images_1 = list(map(lambda b : image[b[1]:b[3], b[0]:b[2]], boxes))
    images_2 = list(map(lambda b : image[b[1]+random.randint(100,170) : b[3], b[0] : b[2]], boxes))
    images_3 = list(map(lambda b : image[b[1] : b[3], b[0]+random.randint(10,50) : b[2]], boxes))
    images_4 = list(map(lambda b : image[b[1]+random.randint(100,170) : b[3], b[0]+random.randint(10,50) : b[2]], boxes))

    image_list = [images_1, images_2, images_3, images_4]
    # image_list = [images_1] 
    num = 0

    print(image.shape)
    print(len(image_list))
    for images in image_list:
        for img, label in zip(images, labels):
            num = num + 1
            cv2.imwrite('{}/{}/{}_{}_{}_{}.jpg'.format(save_path,label,today,label,left_right, num), img)

    print('Random crop image 함수실행!!!')

def file_count(save_path):
    dir_count = sorted(os.listdir(save_path))
    
    result = []
    for i in dir_count:
        folder_name = i
        files = len(os.listdir(f'{save_path}/{i}'))
        result.append([folder_name, files])
    return result

def getDevicesList():
    devices_list = []

    result = os.popen('v4l2-ctl --list-devices').read()
    result_lists = result.split("\n\n")
    for result_list in result_lists:
        if result_list != '':
            result_list_2 = result_list.split('\n\t')
            devices_list.append(result_list_2[1][-1])
    return devices_list

def nothing(x):
    pass


#active_cam = list(map(lambda x : x[-1], getDevicesList()))
active_cam = getDevicesList()


print(f'현재 활성화 되어있는 카메라는 {active_cam} 입니다.')

frame0 = cv2.VideoCapture(LEFT_CAMERA_NUM)
frame1 = cv2.VideoCapture(RIGHT_CAMERA_NUM)

frame0.set(cv2.CAP_PROP_AUTO_WB, 0)
frame0.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
MJPG_CODEC = 1196444237.0 # MJPG


cv2.namedWindow('Interminds Train Image Collection Program by JW', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Interminds Train Image Collection Program by JW', frame_width,frame_height)

frame0.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)
frame0.set(cv2.CAP_PROP_FOURCC, MJPG_CODEC)
frame0.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
frame0.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
frame0.set(cv2.CAP_PROP_AUTOFOCUS, 0)

frame1.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)
frame1.set(cv2.CAP_PROP_FOURCC, MJPG_CODEC)
frame1.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
frame1.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
frame1.set(cv2.CAP_PROP_AUTOFOCUS, 0)

cv2.createTrackbar('Brightness','Interminds Train Image Collection Program by JW', 100, 200, nothing)



while True:

    frame0.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)
    frame1.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)

    ret0, img0 = frame0.read()
    ret1, img00 = frame1.read()


    img0_pi = copy.deepcopy(img0)
    img00_pi = copy.deepcopy(img00)
    
    box1 = get_boxes('./boxes')['{}'.format(BOX_NUM_1)]
    box2 = get_boxes('./boxes')['{}'.format(BOX_NUM_2)]

    box_name = sorted(os.listdir('./boxes'))
    
    # 라벨 커스터마이징 할 때 사용
    # LABELS_left = get_labels('./label_left.txt')
    # LABELS_right = get_labels('./label_right.txt')

    # 음료 및 상온 2221 구조에서 사용
    LABELS_left = get_multi_labels('./label.txt')[0]
    LABELS_right = get_multi_labels('./label.txt')[1]


    blank_image_1 = np.zeros((150, frame_width, 3), np.uint8)
    blank_image_2 = np.zeros((150, frame_width, 3), np.uint8)

    if MODE =='b':
        #textSize1 = textSize2 = -60
        
        for i in box1:
            cv2.rectangle(img0, (i[0],i[1]), (i[2], i[3]), (0,0,255), 2)
    
        for i in box2:
            cv2.rectangle(img00, (i[0],i[1]), (i[2], i[3]), (0,0,255), 2)


    textSize1 = textSize2 = -60
    for j in LABELS_left:
        cv2.putText(blank_image_1, '{} /'.format(j), (textSize1 + 70, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        label_len = cv2.getTextSize(text=str(j+'//'), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, thickness=2)[0][0]
        textSize1 = label_len + textSize1

    for j in LABELS_right:
        cv2.putText(blank_image_2, '{} /'.format(j), (textSize2 + 70, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        label_len = cv2.getTextSize(text=str(j+'//'), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, thickness=2)[0][0]
        textSize2 = label_len + textSize2

    # 박스name 표시
    cv2.putText(blank_image_1, 'BOX : {}_{}'.format(BOX_NUM_1, box_name[int(BOX_NUM_1)]), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,255,0), 3, cv2.LINE_AA)
    cv2.putText(blank_image_2, 'BOX : {}_{}'.format(BOX_NUM_2, box_name[int(BOX_NUM_2)]), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,255,0), 3, cv2.LINE_AA)

    img1 = cv2.resize(img0,(1920,1080))
    img2 = cv2.resize(img00,(1920,1080))

    concated_img1 = cv2.vconcat([blank_image_1, img1])
    concated_img2 = cv2.vconcat([blank_image_2, img2])
    
    rst = cv2.hconcat([concated_img1, concated_img2])
    blank_image_down = np.zeros((500, rst.shape[1], 3), np.uint8)

    folder_text_size = -60
    h = 100
    for i in file_count(save_dir):
        
        cv2.putText(blank_image_down, f'{i[0]} : {i[1]} /', (folder_text_size + 70, h), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)    
        folder_len = cv2.getTextSize(text=str(f'{i[0]} : {i[1]} / '), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, thickness=2)[0][0]
        folder_text_size = folder_len + folder_text_size
        
        if folder_text_size >= rst.shape[1] - 800:
            h = h + 50
            folder_text_size = -60


        # if folder_text_size < rst.shape[1]:
        #     cv2.putText(blank_image_down, f'{i[0]} : {i[1]} /', (folder_text_size + 70, h), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)    
        #     folder_len = cv2.getTextSize(text=str(f'{i[0]} : {i[1]} / '), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, thickness=2)[0][0]

        #     folder_text_size = folder_len + folder_text_size
        #     print(folder_text_size)
        # else:
        #     h = h + 50
        #     folder_text_size = -60
            
        #     cv2.putText(blank_image_down, f'{i[0]} : {i[1]} /', (folder_text_size + 70, h), cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 1, cv2.LINE_AA)    
        #     folder_len = cv2.getTextSize(text=str(f'{i[0]} : {i[1]} / '), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, thickness=2)[0][0]

        #     folder_text_size = folder_len + folder_text_size

    cv2.putText(blank_image_down, 'Brightness : {}'.format(BRIGHTNESS), (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,255,0), 2, cv2.LINE_AA)

    rst = cv2.vconcat([rst, blank_image_down])

    BRIGHTNESS = cv2.getTrackbarPos('Brightness', 'Interminds Train Image Collection Program by JW') - 100

    cv2.imshow('Interminds Train Image Collection Program by JW', rst)
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
   
    ch = cv2.waitKey(1)

######################################################################################################################
    # 종료
    if ch == ord('q'):
	    break

    # 박스 숨기기 / 나타내기
    elif ch == ord('a'):
        if MODE == 'b':
            MODE = 'a'
        else:
            MODE = 'b'


    # box 변경 ( '[' : - 변경,   ']' : + 변경)
    elif ch == ord('o'):
        BOX_NUM_1 = str(int(BOX_NUM_1) + 1)
    
        if BOX_NUM_1 == str(len(os.listdir('./boxes'))):
            BOX_NUM_1 = '0'

    elif ch == ord('p'):
        BOX_NUM_1 = str(int(BOX_NUM_1) - 1)
    
        if BOX_NUM_1 == '-1':
            BOX_NUM_1 = str(len(os.listdir('./boxes'))-1)

    elif ch == ord('['):
        BOX_NUM_2 = str(int(BOX_NUM_2) + 1)
    
        if BOX_NUM_2 == str(len(os.listdir('./boxes'))):
            BOX_NUM_2 = '0'

    elif ch == ord(']'):
        BOX_NUM_2 = str(int(BOX_NUM_2) - 1)
    
        if BOX_NUM_2 == '-1':
            BOX_NUM_2 = str(len(os.listdir('./boxes'))-1)

    elif ch == ord('1'):
        if MODE == 'a':
            image = img1
            
            for label in LABELS_left:
                make_folder(label)

            #crop_image(image, box, save_dir,  LABELS, (RESIZE,RESIZE))
            image_name = './saved_images/left_section_{}.jpg'.format(today)
            cv2.imwrite(image_name, image)
            #crop_random_image(image, box1, save_dir,  LABELS_left)
            print('{} : left section cropped'.format(LABELS_left))
        else:
            print('a 키를 눌러 박스를 제거하고 촬영')        

    elif ch == ord('2'):
        if MODE == 'a':
            image = img2
            
            for label in LABELS_right:
                make_folder(label)

            #crop_image(image, box, save_dir,  LABELS, (RESIZE,RESIZE))
            image_name = './saved_images/right_section_{}.jpg'.format(today)
            cv2.imwrite(image_name, image)
            #crop_random_image(image, box2, save_dir,  LABELS_right)
            print('{} : right section cropped'.format(LABELS_right))
        else:
            print('a 키를 눌러 박스를 제거하고 촬영')


    elif ch == ord('d'):
        if MODE == 'a':
            cv2.imwrite(save_dir_pullimg_l + "/" + today + "_left.jpg", img0_pi)
            cv2.imwrite(save_dir_pullimg_r + "/" + today + "_right.jpg", img00_pi)
          
            image1 = img1
            image2 = img2
            
            for label in LABELS_right:
                make_folder(label)
            for label in LABELS_left:
                make_folder(label)        

            #crop_image(image, box, save_dir,  LABELS, (RESIZE,RESIZE))
            crop_random_image(image1, box1, save_dir,  LABELS_left, left_right='left')
            #time.sleep(1)
            crop_random_image(image2, box2, save_dir,  LABELS_right, left_right='right')
            print('{} // {} : left, right section cropped'.format(LABELS_left, LABELS_right))
        else:
            print('a 키를 눌러 박스를 제거하고 촬영')

    # 트랙바로 대체
    # elif ch == ord('+'):
    #     BRIGHTNESS = BRIGHTNESS + 2
    #     print(BRIGHTNESS)
    
    # elif ch == ord('-'):
    #     BRIGHTNESS = BRIGHTNESS -2
    #     print(BRIGHTNESS)

    elif ch == ord('f'):
        if MODE == 'a':
            image_name = './saved_images/left_box_{}.jpg'.format(today)
            cv2.imwrite(image_name, img1)
            os.system('python3 ./labelimg/labelImg.py {} ./labelimg/data/predefined_classes.txt ./boxes'.format(image_name))

        else:
            print('a 키를 눌러 박스를 제거하고 촬영')

    elif ch == ord('g'):
        if MODE == 'a':
            image_name = './saved_images/right_box_{}.jpg'.format(today)
            cv2.imwrite(image_name, img2)
            os.system('python3 ./labelimg/labelImg.py {} ./labelimg/data/predefined_classes.txt ./boxes'.format(image_name))

        else:
            print('a 키를 눌러 박스를 제거하고 촬영')



frame0.release()
frame1.release()
cv2.destroyAllWindows()
