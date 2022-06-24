import os

import yolov5_face

class App:
    def __init__(self, path): #конфиг по умолчанию
        self.__video_path = path

    def start_ai(self):
        yolov5_model = yolov5_face.AI_Yolov5()
        yolov5_model.find_faces_from_video()


if __name__ == '__main__':
    app = App('training_video.mp4')
    app.start_ai()