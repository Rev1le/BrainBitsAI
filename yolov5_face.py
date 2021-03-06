from yolov5facedetector.face_detector import YoloDetector

import numpy as np
from PIL import Image
import cv2
import uuid
import os
import shutil
import json
from emotions import Detector
from threading import Thread
from asyncio import *
import json
import time
import plots


class AI_Yolov5():
    cont = True

    def __init__(self, config='config.json'):
        with open(config, encoding='utf-8') as f:
            const_data = json.load(f)
        self.detector = Detector('cpu')
        self.emotions_list = []
        self.emotions_dict_json = {}

        self.PATH_PROJECT: str = os.getcwd()
        #self.PATH_FOR_FACES: str = const_data['path_for_faces']  # Устарело, теперь нет необходимоти сохранять фотки
        self.MIN_FACE_PERCENT: int = const_data['min_face_percent']
        self.SAVING_FRAMES_PER_SECOND: int = const_data['fps_received']

        self.model = YoloDetector(gpu=0, min_face=self.MIN_FACE_PERCENT)
        self.fasec_image_list = []

        self.plots = plots.plots()

    def add_emotion_to_list(self, emotion):
        self.emotions_list.append(emotion)

        print(self.emotions_list)
        print('Время выполнения',self.start_time - time.time())


    @property
    def get_emotions_list(self):
        return self.emotions_list

    def save_json_emotions(self):
        json_string = json.dumps(self.emotions_dict_json)
        with open('emotions.json', "w+") as f:
            f.write(json_string)
        return self.emotions_dict_json

    def analysis_image(self, img_array, frame_time):
        img_nparray_rgb = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img_nparray_rgb).convert('RGB')#Image.open(path_frame_tmp)
        bboxes, confs, points = self.model.predict(img_array)

        list_face_coords: list = bboxes[0]
        print(list_face_coords)
        ###
        # Получаем массив картинок формата Image для каждого полученного фрейма
        ###
        list_face = self.create_list_image(list_face_coords, image)

        if len(list_face) > 0:
            result_emotions = self.detector.detect_emotion(list_face, self.add_emotion_to_list, True)
            self.emotions_dict_json[frame_time] = result_emotions
            print(self.emotions_dict_json)
            for emotion in result_emotions:
                self.add_emotion_to_list(emotion)

        return True


    def create_list_image(self, list_nparray, target_img):
        list_image = []
        for face_coords in list_nparray:
            face_standart_coords = self.format_coords(face_coords)
            face_img = target_img.crop((face_standart_coords)).resize((512, 512))
            list_image.append(face_img)
        return list_image

    # Устарело из-за ненадобности сохранять лица
    '''
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

    '''

    def find_faces_from_video(self, path, video_length, view_json_method = None, second_tk =None , update = None):
        print("Видео для обработки", path())
        print('Длина видео ', video_length())
        rtspVideo = cv2.VideoCapture(path())
        self.PATH_TRAINING_VIDEO = path
        current_frame_number = 0
        count = 0

        print('Всего кадров в идео', rtspVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        print('Кадров в секунду в видео', rtspVideo.get(cv2.CAP_PROP_FPS))

        fps = rtspVideo.get(cv2.CAP_PROP_FPS)
        all_frame_video = rtspVideo.get(cv2.CAP_PROP_FRAME_COUNT)

        delay_time = 1

        try:
            second_tk()
        except Exception:
            pass

        if video_length() == 'short':
            print('видео короткое')
            delay_time = int(fps * 1)+1
        elif video_length() == 'long':
            print('видео длинное')
            delay_time = int(fps * 5)+1

        self.clean_folder_faces()

        while rtspVideo.isOpened():
            ret, frame_nparray = rtspVideo.read()
            current_frame_number += 1


            if ret:
                count += 1
            else:
                print('Frame read failed')
                break

            if count == delay_time:
                #update()
                try:
                 second_tk()
                except Exception:
                    pass
                #view_json_method()
                self.plots.create_pirog(self.emotions_list)
                #print(current_frame_number)
                self.start_time = time.time()
                frame_time = int(current_frame_number / fps)
                #print(frame_time)
                # img = cv2.cvtColor(frame_nparray.astype(np.uint8), cv2.COLOR_BGR2RGB)
                self.analysis_image(frame_nparray, frame_time)
                count = 0

            if count == 40 :
                self.save_json_emotions()
        return self.save_json_emotions()

    @staticmethod
    def format_coords(coords: list):
        assert (len(coords) == 4)
        delta_y = coords[3] - coords[1]  # d = y2 - x1 (длина большей стороны)
        delta_x = coords[2] - coords[0]  # d = x2 - x1

        increase = int((delta_y - delta_x) // 2) + 5

        coords[0] -= increase
        coords[1] += increase

        return coords

def start_ai(path):
    yolov5 = AI_Yolov5()
    yolov5.find_faces_from_video(path=path)