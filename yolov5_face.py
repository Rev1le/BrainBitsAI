from yolov5facedetector.face_detector import YoloDetector

import numpy as np
from PIL import Image
import cv2
import uuid
import os
import shutil
import json


class AI_Yolov5():

    def __init__(self, config='config.json'):
        with open(config, encoding='utf-8') as f:
            const_data = json.load(f)

        self.PATH_PROJECT: str = os.getcwd()
        self.PATH_FOR_FACES: str = const_data['path_for_faces']
        self.MIN_FACE_PERCENT: int = const_data['min_face_percent']
        self.PATH_TRAINING_VIDEO: str = const_data['path_url_training_video']
        self.SAVING_FRAMES_PER_SECOND: int = const_data['fps_received']

        self.model = YoloDetector(gpu=0, min_face=self.MIN_FACE_PERCENT)
        self.fasec_image_list = []

    # def analysis_image(self, img_array):
    #     path_frame_tmp: str = f'{self.PATH_PROJECT}\\frame.jpg'
    #     cv2.imwrite(path_frame_tmp, img_array)
    #     image = Image.open(path_frame_tmp)
    #
    #     bboxes, confs, points = self.model.predict(img_array)
    #
    #     list_face_coords: list = bboxes[0]
    #     print(list_face_coords)
    #
    #     self.save_faces(list_face_coords, image)
    #     return True

    def analysis_image(self, img_array):
        path_frame_tmp: str = f'{self.PATH_PROJECT}\\frame.jpg'
        #cv2.imwrite(path_frame_tmp, img_array)
        img_nparray_rgb = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img_nparray_rgb).convert('RGB')#Image.open(path_frame_tmp)
        bboxes, confs, points = self.model.predict(img_array)

        list_face_coords: list = bboxes[0]
        print(list_face_coords)

        self.save_faces(list_face_coords, image)
        return True

    def save_faces(self, list_face_coords, image):
        for face_coords in list_face_coords:
            # стандартизация лиц
            face_standart_coords = self.format_coords(face_coords)
            cropped_img = image.crop((face_standart_coords)).resize((512, 512))
            #cropped_img = cropped_img.resize((512, 512))
            cropped_img.save(f"{self.PATH_FOR_FACES}\\лицо_{uuid.uuid4()}.jpg", quality=95)
            self.fasec_image_list.append(cropped_img)
        return True

    def clean_folder_faces(self):
        file_path_folder = self.PATH_FOR_FACES
        try:
            shutil.rmtree(file_path_folder)
        except FileNotFoundError :
            print("удаление паки с лицами не было произведено")
        os.mkdir(file_path_folder)
        #print(file_path_folder.split('\\')[-1])

    def find_faces_from_video(self):
        rtspVideo = cv2.VideoCapture(self.PATH_TRAINING_VIDEO)

        print(rtspVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        print(rtspVideo.get(cv2.CAP_PROP_FPS))

        count: int = 0

        self.clean_folder_faces()

        while rtspVideo.isOpened():
            ret, frame_nparray = rtspVideo.read()

            if ret:
                count += 1
            else:
                print('Frame read failed')
                break

            if count == 30:
                #img = cv2.cvtColor(frame_nparray.astype(np.uint8), cv2.COLOR_BGR2RGB)
                self.analysis_image(frame_nparray)
                count = 0
        return self.fasec_image_list

    @staticmethod
    def format_coords(coords: list):
        assert (len(coords) == 4)
        delta_y = coords[3] - coords[1]  # d = y2 - x1 (длина большей стороны)
        delta_x = coords[2] - coords[0]  # d = x2 - x1

        increase = int((delta_y - delta_x) // 2) + 5

        coords[0] -= increase
        coords[1] += increase

        return coords
