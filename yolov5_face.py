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


class AI_Yolov5():

    def __init__(self, config='config.json'):
        with open(config, encoding='utf-8') as f:
            const_data = json.load(f)
        self.detector = Detector('cpu')
        self.emotions_list = []

        self.PATH_PROJECT: str = os.getcwd()
        self.PATH_FOR_FACES: str = const_data['path_for_faces']
        self.MIN_FACE_PERCENT: int = const_data['min_face_percent']
        self.PATH_TRAINING_VIDEO: str = const_data['path_url_training_video']
        self.SAVING_FRAMES_PER_SECOND: int = const_data['fps_received']

        self.model = YoloDetector(gpu=0, min_face=self.MIN_FACE_PERCENT)
        self.fasec_image_list = []

    def add_emotion_to_list(self, emotion):
        self.emotions_list.append(emotion)
        print(self.emotions_list)

    @property
    def get_emotions_list(self):
        return self.emotions_list

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
            self.detector.detect_emotion(list_face,self.add_emotion_to_list, True)

        threads_list =[]
        # if len(list_face) <= 5 :
        #     for face in list_face:
        #         thread = Thread(target=self.detector.detect_emotion, args= ([face],self.add_emotion_to_list, True), daemon=True)
        #         threads_list.append(thread)
        #         thread.start()
        # else :
        #     for ind, face in enumerate(list_face):
        #         thread = Thread(target=self.detector.detect_emotion, args= ([face],self.add_emotion_to_list, True), daemon=True)
        #         threads_list.append(thread)
        #         thread.start()
        #         if ind == 4 : break

        #for thread in threads_list:  # iterates over the threads
        #    thread.join()
        #    print(thread.is_alive())

            #for face in list_face:
        #    face.show()
        return True


    def create_list_image(self, list_nparray, target_img):
        list_image = []
        for face_coords in list_nparray:
            face_standart_coords = self.format_coords(face_coords)
            face_img = target_img.crop((face_standart_coords)).resize((512, 512))
            list_image.append(face_img)
        return list_image

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

    def find_faces_from_video(self, path):
        rtspVideo = cv2.VideoCapture(path)#self.PATH_TRAINING_VIDEO)
        self.PATH_TRAINING_VIDEO = path

        print(rtspVideo.get(cv2.CAP_PROP_FRAME_COUNT))
        print(rtspVideo.get(cv2.CAP_PROP_FPS))

        fps = rtspVideo.get(cv2.CAP_PROP_FPS)
        all_frame_video = rtspVideo.get(cv2.CAP_PROP_FRAME_COUNT)

        current_frame_number =0

        video_time = all_frame_video / fps

        n_fps = 0.5*video_time

        cadr_num = (video_time// n_fps)*fps
        print(cadr_num)

        count: int = 0
        n = 1

        self.clean_folder_faces()

        while rtspVideo.isOpened():
            ret, frame_nparray = rtspVideo.read()
            current_frame_number+=1


            if ret:
                count += 1
            else:
                print('Frame read failed')
                break

            if count == int(fps*n):
                frame_time = current_frame_number//fps
                #img = cv2.cvtColor(frame_nparray.astype(np.uint8), cv2.COLOR_BGR2RGB)
                self.analysis_image(frame_nparray, frame_time)
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

def start_ai(path):
    yolov5 = AI_Yolov5()
    yolov5.find_faces_from_video(path=path)