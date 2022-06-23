from yolov5facedetector.face_detector import YoloDetector

import numpy as np
from PIL import Image
from random import randint
import cv2

SAVING_FRAMES_PER_SECOND = 10

def analysis_image(img_array):
    bboxes, confs, points = model.predict(img_array)
    list_face_coords: list = bboxes[0]
    print(list_face_coords)
    cv2.imwrite(f'D:\\Project\\Python\\AI\\frame.jpg', img_array)
    image = Image.open(f'D:\\Project\\Python\\AI\\frame.jpg')
    save_faces(list_face_coords, image)
    return True

def save_faces(list_face_coords, image):
    for face_coords in list_face_coords:
        cropped_img = image.crop((face_coords))
        cropped_img = cropped_img.resize((512, 512))
        cropped_img.save(f"D:\\Project\\Python\\AI\\лица\\лицо{randint(0, 99999)}.jpg",  quality=95)
    return True



model = YoloDetector(gpu=0, min_face=50) # Will download weight file automatically


video_path = "D:\\Project\\Python\\AI\\traning_video.mp4"
rtspVideo = cv2.VideoCapture(video_path)

print(rtspVideo.get(cv2.CAP_PROP_FRAME_COUNT))
print(rtspVideo.get(cv2.CAP_PROP_FPS))

count: int = 0

while rtspVideo.isOpened():
    ret, frame_nparray = rtspVideo.read()

    if ret:
        count += 1
    else:
        print("frame read failed")
        break

    if count == 30:

        analysis_image(frame_nparray)
        count = 0
