import asyncio

from yolov5facedetector.face_detector import YoloDetector

import numpy as np
from PIL import Image
import cv2
import uuid
import os, shutil
from emotions import Detector
import time
import plots
import json
from asyncio import *
#from threading import Thread



class AI_Yolov5():
    cont = True

    def __init__(self, config='config.json'):
        with open(config, encoding='utf-8') as f:
            const_data = json.load(f)
        self.detector = Detector('cpu')
        self.emotions_list = []
        self.emotions_dict_json = {}

        self.PATH_PROJECT: str = os.getcwd()
        self.PATH_FOR_FACES: str = const_data['path_for_faces']
        self.MIN_FACE_PERCENT: int = const_data['min_face_percent']
        #self.SAVING_FRAMES_PER_SECOND: int = const_data['fps_received']

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
        path_frame_tmp: str = f'{self.PATH_PROJECT}\\frame.jpg'
        #cv2.imwrite(path_frame_tmp, img_array)
        img_nparray_rgb = cv2.cvtColor(img_array.astype(np.uint8), cv2.COLOR_BGR2RGB)
        image = Image.fromarray(img_nparray_rgb).convert('RGB')#Image.open(path_frame_tmp)
        bboxes, confs, points = self.model.predict(img_array)

        list_face_coords: list = bboxes[0]
        print(list_face_coords)

        #self.save_faces(list_face_coords, image)
        ###
        # Получаем массив картинок формата Image для каждого полученного фрейма
        ###
        list_face = self.create_list_image(list_face_coords, image)

        if len(list_face) > 0:
            #self.detector.asinhron_detect_emotion()
            #result_emotions = self.detector.detect_emotion(list_face, self.add_emotion_to_list, True)
            #for face in list_face:
            #    self.detector.asinhron_detect_emotion()

            #try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.emo_detect_async(list_face, loop))
            #except:
            #    pass


            #result_emotions = self.detector.asinhron_detect_emotion(list_face, self.add_emotion_to_list, True)
            #self.emotions_dict_json[frame_time] = result_emotions
            #print(self.emotions_dict_json)
            #for emotion in result_emotions:
            #    self.add_emotion_to_list(emotion)
        return True

    async def emo_detect_async(self, list_face, loop):
        task_list = []
        for ind, face in enumerate(list_face):
            task = loop.create_task(self.async_func(ind, face, self.add_emotion_to_list))
            task_list.append(task)
        await asyncio.wait(task_list)
        return

    async def async_func(self,ind_task, face, func_add_emo_to_list):
        print(f'{ind_task}: Запуск ...')
        self.detector.detect_emotion(face, func_add_emo_to_list, True)
        print(f'{ind_task}: Завершено ...')
        return


    def create_list_image(self, list_nparray, target_img):
        list_image = []
        for face_coords in list_nparray:
            face_standart_coords = self.format_coords(face_coords)
            face_img = target_img.crop((face_standart_coords)).resize((512, 512))
            list_image.append(face_img)
        return list_image


    def save_faces(self, list_face_coords, image):
        for face_coords in list_face_coords:
            # стандартизация лиц для обработки эмоций
            face_standart_coords = self.format_coords(face_coords)
            cropped_img = image.crop((face_standart_coords)).resize((512, 512))
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

    def find_faces_from_video(self, path, video_length, view_json_method = None, second_tk =None , update = None):
        print("Видео для обработки", path())
        print('Видео считается ', video_length())
        rtspVideo = cv2.VideoCapture(path())
        self.PATH_TRAINING_VIDEO = path
        current_frame_number = 0
        count = 0
        delay_time = 1

        print('Всего кадров в видео', rtspVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        print('Кадров в секунду в видео', rtspVideo.get(cv2.CAP_PROP_FPS))

        fps = rtspVideo.get(cv2.CAP_PROP_FPS)
        all_frame_video = rtspVideo.get(cv2.CAP_PROP_FRAME_COUNT)


        #try:
        #    second_tk()
        #except Exception:
        #    pass

        if video_length() == 'short':
            print('Обработка короткого видео')
            delay_time = int(fps * 1)+1
        elif video_length() == 'long':
            print('Обработка длинного видео')
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

                #try:
                #    second_tk()
                #except Exception:
                #    pass

                #self.plots.create_pirog(self.emotions_list)
                self.start_time = time.time() # Время начала анализа данных
                global_frame_time = int(current_frame_number / fps)
                self.analysis_image(frame_nparray, global_frame_time)
                count = 0

            if count == 40: self.save_json_emotions() #Сохранение резулттата каждые 40 секунд
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