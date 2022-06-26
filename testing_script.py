import yolov5_face
import os
yolo5_face = yolov5_face.AI_Yolov5()

global path

emotions = ("angry","disgust","fear","happy","sad","surprise","neutral")


def get_path_video():
    global path
    return path



def set_path(pathFile: str):
    global path
    path = pathFile


def get_video_lenght():
    return 'short'

def list_file():
    for dirname, _, filenames in os.walk(input('Введите путь до папки с файлами')):
            list_file=[os.path.join(dirname, filename) for filename in filenames]
    return list_file

for i in list_file():
    set_path(i)
    regular = '(.*)'
    print(yolo5_face.find_faces_from_video(path = get_path_video, video_length=get_video_lenght))