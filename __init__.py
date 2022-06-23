from yolov5facedetector.face_detector import YoloDetector

import numpy as np
from PIL import Image
from random import randint
import time
model = YoloDetector(gpu=0, min_face=60) # Will download weight file automatically

def search_face(bboxes, resize_img):
    print(bboxes)
    for i in range(len(bboxes[0])):
        print(bboxes[0][i])
        coord = bboxes[0][i]
        x = (coord[0] + coord[2])
        y = (coord[1] + coord[3])
        delt = (coord[3] - coord[1])
        square_coord =coord# [x-delt//2, y-delt//2, x+delt//2, y+delt//2]
        cropped_img = resize_img.crop((square_coord))
        cropped_img = cropped_img.resize((112, 112))
        print("сохраняется")
        #time.sleep(1)
        cropped_img.save(f"лица\\лицо{randint(0, 99999)}.jpg",  quality=95)
        list_face.append(cropped_img)
    return list_face
        # cropped_img.show()
        # cropped_img.save(f'face{i}.jpg', quality=95)

list_face = []
def recognizeFace(frame):
    img = Image.open(frame)
    resize_img = img #img.resize((img.size[0]//32*32, (img.size[1]//32)*32))
    rgb_array_img = np.array(resize_img) # Will make RGB Numpy Array Image
    bboxes, confs, points = model.predict(rgb_array_img)
    print(bboxes)
    list_face = search_face(bboxes, resize_img)
    return list_face

# recognizeFace('frame.jpg')


import cv2
rtspVideo = cv2.VideoCapture("ddc8027b-7cac-468c-82f0-eb5e5ea0b78a.mp4")
while rtspVideo.isOpened():
    # Read video capture
    i = 0
    if i // 30 == 0:    
        ret, frame = rtspVideo.read()
        if ret:
            # The frame is ready and already captured
            #cv2.imshow('video', frame)
            cv2.imwrite('frame.jpg', frame)
            print("получаю кадр")
            list_face = recognizeFace('frame.jpg')
            #print(frame)
    else:
        i += 1
