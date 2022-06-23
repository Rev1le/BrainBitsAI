from yolov5facedetector.face_detector import YoloDetector

import numpy as np
from PIL import Image
import cv2
import uuid
import os
import shutil
import json


with open("config.json", encoding='utf-8') as f:
    const_data = json.load(f)

PATH_PROJECT = os.getcwd()
PATH_FOR_FACES = const_data['path_for_face']
MIN_FACE_PERCENT = const_data['min_face_percent']
PATH_TRAINING_VIDEO = const_data['path_url_training_video']
SAVING_FRAMES_PER_SECOND = const_data['fps_received']

def analysis_image(img_array):
    bboxes, confs, points = model.predict(img_array)
    list_face_coords: list = bboxes[0]
    print(list_face_coords)

    path_frame_tmp: str = f'{PATH_PROJECT}\\frame.jpg'
    cv2.imwrite(path_frame_tmp, img_array)
    image = Image.open(path_frame_tmp)

    save_faces(list_face_coords, image)
    return True

def save_faces(list_face_coords, image):
    for face_coords in list_face_coords:
        cropped_img = image.crop((face_coords))
        cropped_img = cropped_img.resize((512, 512))
        cropped_img.save(f"{PATH_FOR_FACES}\\лицо_{uuid.uuid4()}.jpg",  quality=95)
    return True

def clean_folder_faces():
    file_path_folder = PATH_FOR_FACES
    shutil.rmtree(file_path_folder)
    os.mkdir(file_path_folder)


model = YoloDetector(gpu=0, min_face=70) # Will download weight file automatically

rtspVideo = cv2.VideoCapture(PATH_TRAINING_VIDEO)

print(rtspVideo.get(cv2.CAP_PROP_FRAME_COUNT))
print(rtspVideo.get(cv2.CAP_PROP_FPS))

count: int = 0

clean_folder_faces()

while rtspVideo.isOpened():
    ret, frame_nparray = rtspVideo.read()

    if ret: count += 1
    else:
        print("Frame read failed")
        break

    if count == 30:
        analysis_image(frame_nparray)
        count = 0
