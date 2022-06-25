import yolov5_face
import gui
from threading import Thread
from tkinter import *


class App:
    ''''Основной класс приложения'''

    @staticmethod
    def start_app() -> None:
        yolov5_model: object = yolov5_face.AI_Yolov5()
        graphics_interface: object = gui.GUI()


        # Поток для обработки данных был создан вы класе APP, из-за поблем с созданием его в классе GUI
        # GUI зависало намертво из-за незаконченной функции
        thread_yolov_ai = Thread(target=yolov5_model.find_faces_from_video,  # Создаем поток для нейронки
                                 args=[graphics_interface.get_video_path,
                                       graphics_interface.get_lenght_video],  # Возвращает путь к видео
                                 daemon=True)
        #print(type(graphics_interface.get_video_path))

        graphics_interface.start_gui(AI_thread=thread_yolov_ai)  # Запуск интерфейса программы


if __name__ == '__main__':
    App.start_app()
