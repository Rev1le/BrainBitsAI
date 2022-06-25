import os

import yolov5_face
import gui
from threading import Thread


class App:
    def __init__(self, path): #конфиг по умолчанию
        self.__video_path = path


    def start_ai(self):
        yolov5_model = yolov5_face.AI_Yolov5()

        thread_yolov_ai = Thread(target=yolov5_model.find_faces_from_video)
        thread_gui = Thread(target=gui.start_gui)
        thread_yolov_ai.start()
        thread_gui.start()


if __name__ == '__main__':
    app = App('training_video.mp4')
    app.start_ai()