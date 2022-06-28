import time
from threading import Thread
from tkinter import *
from tkinter import filedialog
import yolov5_face
import asyncio
#from PIL import ImageTk
#from emotions import Detector
#import cv2
#import numpy as np
#import json
#from tk import *
#import os


class widjets():
    '''Класс для создания виджетов - говно полное'''

    def create_button_place(self, frame: Canvas, command, image: str = None, x: int = 0, y: int = 0, anchor: str = 'nw',
                            text: str = '') -> None:

        if image is not None:
            self.img = PhotoImage(file=f'button_img\\{image}')

            self.btn = Button(frame, activebackground='#313538', bg='#313538',
                   image=self.img, command=command,
                   relief='flat', borderwidth=0).place(x=x, y=y, anchor=anchor)
        else:
            self.btn = Button(frame, activebackground='#313538', bg='#313538', command=command, relief='flat',
                   borderwidth=0).place(x=x, y=y, anchor=anchor)

    def create_label(self, frame: Tk, x: int, y: int, text: str = '', width: int = 25, height: int = 1,
                     font: tuple = ("MS Sans Serif", 14), bg: str = 'white', fg: str = '#05aeb8',
                     anchor: str = 'w') -> None:

        self.lbl = Label(frame, text=text, width=width, height=height,
                         font=font, bg=bg, fg=fg, anchor=anchor).\
                         place(x=x, y=y, anchor=anchor)


class GUI(widjets):
    '''класс с ткинтером. Здесь из необходимого тебе - это метод view_json'''

    #__video_path_private = ''

    def __init__(self, name: str = 'BrainBits', width: int = 1280, height: int = 720,
                 change_size: dict = {'width': False,
                                      'height': False}) -> None:
        self.window = Tk()
        self.window.title(name)
        self.canvas = Canvas(self.window, bg='#313538', width=1281, height=721)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.window.resizable(change_size['width'], change_size['height'])
        self.window.geometry(f'{width}x{height}+300+100')

        self.yolov5 = yolov5_face.AI_Yolov5()


    def get_video_path(self):
        return self.__video_path_private
    def get_lenght_video(self):
        return self.__lenght_video

    async def thread_yolov(self):
        thr = Thread(target=self.yolov5.find_faces_from_video,  # Создаем поток для нейронки
                                 args=[self.get_video_path,
                                       self.get_lenght_video,
                                       self.view_json,
                                       self.second_tk,
                                       self.update],  # Возвращает путь к видео
                                 daemon=True)
        thr.start()
        #thr.join()


    def start_gui(self):#, AI_thread):
        # Yolov5 = yolov5_face.AI_Yolov5()
        # emo_detect = Detector('cpu')

        def command_button(lenght_video):
            self.__lenght_video = lenght_video
            path = self.browseFiles()
            asyncio.run(self.thread_yolov())
            #AI_thread.start()  # Начинаем обработку видео
            #AI_thread.join()
            #self.view_json(json.loads('{"a": 5, "b": 7}'))

        short_video = lambda : command_button('short')
        long_video = lambda : command_button('long')

        # Создание экземпляра кнопок
        wid = widjets()
        wid1 = widjets()
        wid2 = widjets()

        # Создание самих кнопок
        wid.create_label(frame=self.get_canvas(), x=450, y=0,
                         text='BrainBits', bg='#313538', fg='#FFFFFE',
                         font=("MS Sans Serif", 76), anchor='nw')

        wid.create_button_place(frame=self.get_canvas(),
                                image='button1.gif', command=long_video,
                                x=332, y=370)

        wid1.create_button_place(frame=self.get_canvas(),
                                 image='OneEmotion.gif', command=short_video,
                                 x=650, y=370)

        wid2.create_button_place(frame=self.get_canvas(),
                                 image='Exit.gif', command=self.destroy,
                                 x=1050, y=600)
        self.mainloop()

    def update(self):
        try:
            # self.img = PhotoImage("pie.png")
            # self.panel = Label(self.win, image=self.img)
            self.img = PhotoImage(file= r"C:\Users\nikiy\Desktop\Hackaton\BrainBitsAI\pie.png")
            #self.panel.update() #= Label(self.win, image=self.img)
            #panel.pack(side='top')
        except TclError:
            pass


    def second_tk(self):
        self.win = Toplevel(self.window)
        self.win.geometry('640x480+700+300')
        self.win.resizable(False, False)
        try:
            # self.img = PhotoImage("pie.png")
            # self.panel = Label(self.win, image=self.img)
            # self.panel.pack(side="bottom")
            self.img = PhotoImage(file=r"C:\Users\nikiy\Desktop\Hackaton\BrainBitsAI\pie.png")
            self.panel = Label(self.win, image=self.img)
            #self.panel.image = self.img
            self.panel.pack(side='top')
            time.sleep(0.8)
            self.win.destroy()
        except TclError:
            pass

    def view_json(self) -> None:
        '''этот метод создаёт дочерее окно с текстовым полем и читает предполагаемый json (надо настроить)'''

        self.win = Toplevel(self.window)
        self.win.geometry('640x480+700+300')
        self.win.resizable(False, False)
        self.img = PhotoImage("pie.png")
        print(img)
        self.panel = Label(win, image=img)
        self.panel.pack()
        #win.mainloop()
        # c = Canvas(win, height=480, width=640, bg='white')
        # c.pack()
        # text = Text(c)
        # text.pack()
        # for k in json:
        #     text.insert(END, '{} = {}\n'.format(k, json[k]))
        # text.config(state=DISABLED)

    def browseFiles(self):
        path = filedialog.askopenfilename(initialdir="/", title="Select file", \
                                          filetypes=(("mp4 files", "*.mp4"), \
                                                     ("jpg files", "*.jpg"), \
                                                     ("jpeg files", "*.jpeg"), \
                                                     ("png files", "*.png"), \
                                                     ("all files", "*.*")))
        print(path)
        self.__video_path_private = path
        return path

    def get_main_window(self):
        return self.window

    def get_canvas(self):
        return self.canvas

    def mainloop(self):
        self.window.mainloop()

    def destroy(self):
        self.window.destroy()


