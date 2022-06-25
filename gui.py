import os
import time
from threading import Thread
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk
from emotions import Detector
import cv2
import numpy as np
import json
import yolov5_face


class GUI():
    '''класс с ткинтером. Здесь из необходимого тебе - это метод view_json'''

    def __init__(self, window: Tk, name: str = 'BrainBits', width: int = 1280, height: int = 720,
                 change_size: dict = {'width': False, 'height': False}) -> None:
        self.window = window
        self.window.title(name)
        self.canvas = Canvas(self.window, bg='#313538', width=1281, height=721)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.window.resizable(change_size['width'], change_size['height'])
        self.window.geometry(f'{width}x{height}+300+100')

    def view_json(self, json: json) -> None:
        '''этот метод создаёт дочерее окно с текстовым полем и читает предполагаемый json (надо настроить)'''

        win = Toplevel(self.window)
        win.geometry('640x480+700+300')
        win.resizable(False, False)
        c = Canvas(win, height=480, width=640, bg='white')
        c.pack()
        text = Text(c)
        text.pack()
        for k in json:
            text.insert(END, '{} = {}\n'.format(k, json[k]))
        text.config(state=DISABLED)

    def get_main_window(self):
        return self.window

    def get_canvas(self):
        return self.canvas

    def mainloop(self):
        self.window.mainloop()

    def destroy(self):
        self.window.destroy()


class widjets():
    '''Класс для создания виджетов - говно полное'''

    def create_button_grid(self, frame: Tk, command, image: str = None, row: int = 0, column: int = 0, rowspan: int = 1,
                           columnspan: int = 1, padx: int = 0, pady: int = 0, text: str = '') -> None:

        if image is not None:
            self.btn = Button(frame, text=text, image=PhotoImage(file=f'button_img\\{image}'), command=command)
            self.btnbtn.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=padx)
        else:
            self.btnbtn = Button(frame, text=text)
            self.btnbtn.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=padx, pady=padx)

    def create_button_place(self, frame: Canvas, command, image: str = None, x: int = 0, y: int = 0, anchor: str = 'nw',
                            text: str = '') -> None:

        if image is not None:
            self.img = PhotoImage(file=f'button_img\\{image}')

            self.btn = Button(frame, activebackground='#313538', bg='#313538', image=self.img, command=command,
                              relief='flat', borderwidth=0).place(x=x, y=y, anchor=anchor)
        else:
            self.btn = Button(frame, activebackground='#313538', bg='#313538', command=command, relief='flat',
                              borderwidth=0).place(x=x, y=y, anchor=anchor)

    def create_label(self, frame: Tk, x: int, y: int, text: str = '', width: int = 25, height: int = 1,
                     font: tuple = ("MS Sans Serif", 14), bg: str = 'white', fg: str = '#05aeb8',
                     anchor: str = 'w') -> None:

        self.lbl = Label(frame, text=text, width=width, height=height, font=font, bg=bg, fg=fg, anchor=anchor).place(
            x=x, y=y, anchor=anchor)

    def create_entry(self, frame: Tk, x: int, y: int, width: int = 25, height: int = 1,
                     font: tuple = ("MS Sans Serif", 14), bg: str = 'white', fg: str = '#05aeb8', anchor: str = 'n'):

        self.entr = Entry(frame, width=width, height=height, font=font, bg=bg, fg=fg).place(x=x, y=y)



#emo_detect = Detector('cpu')
#App = GUI(Tk())
#wid = widjets()
#wid1 = widjets()
#wid2 = widjets()

def start_gui():
    def browseFiles():
        ''' эта функция обрабатывет кнопки. Здесь должны быть два метода поиска эмоций - один для толпы, второй для одного человека.
        Пока что тут запуск проводника и обычное считывание эмоций и запуск дочернего окна с json'ом '''

        # print('здесь будет класс, который примет следующий путь',filedialog.askopenfilename(initialdir="/", title="Select file",
        #                                       filetypes = (("jpg files", "*.jpg"),("jpeg files", "*.jpeg"),("png files", "*.png"),("mp4 files", "*.mp4"),("all files",
        #                                                     "*.*"))))
        #print(emo_detect.detect_emotion \
        #          (np.array([cv2.imread \
        #                         (filedialog.askopenfilename(initialdir="/", title="Select file", \
         #                                                    filetypes=(("jpg files", "*.jpg"), \
        #                                                                ("jpeg files", "*.jpeg"), \
         #                                                               ("png files", "*.png"), \
         #                                                               ("mp4 files", "*.mp4"), \
          #                                                              ("all files", "*.*"))))]), True))
        path = filedialog.askopenfilename(initialdir="/", title="Select file", \
                                        filetypes=(("jpg files", "*.jpg"), \
                                                ("jpeg files", "*.jpeg"), \
                                                ("png files", "*.png"), \
                                                ("mp4 files", "*.mp4"), \
                                                ("all files", "*.*")))
        thread_ai = Thread(target=Yolov5.find_faces_from_video, args=[path], daemon=True)
        thread_ai.start()
        thread_ai.join()
        App.view_json(json.loads('{"a": 5, "b": 7}'))


    # print('поток рабоате')
    # time.sleep(5)
    # print('поток переставл рабоать')
    #exit()
    App = GUI(Tk())
    Yolov5 = yolov5_face.AI_Yolov5()
    emo_detect = Detector('cpu')
    wid = widjets()
    wid1 = widjets()
    wid2 = widjets()
    #App.create_label(frame = App.get_canvas(), x=475,y=0, text = 'BrainBits', bg='#313538', fg = '#FFFFFE', font = ("MS Sans Serif",48), anchor='nw')

    '''создание интрефейса'''
    wid.create_label(frame=App.get_canvas(), x=450, y=0, text='BrainBits', bg='#313538', fg='#FFFFFE',
                     font=("MS Sans Serif", 76), anchor='nw')
    wid.create_button_place(frame=App.get_canvas(), image='button1.gif', command=browseFiles, x=332, y=370)
    wid1.create_button_place(frame=App.get_canvas(), image='OneEmotion.gif', command=browseFiles, x=650, y=370)
    wid2.create_button_place(frame=App.get_canvas(), image='Exit.gif', command=App.destroy, x=1050, y=600)
    App.mainloop()



# App.create_label(frame = App.get_canvas(), x=475,y=0, text = 'BrainBits', bg='#313538', fg = '#FFFFFE', font = ("MS Sans Serif",48), anchor='nw')

'''создание интрефейса'''
# wid.create_label(frame=App.get_canvas(), x=450, y=0, text='BrainBits', bg='#313538', fg='#FFFFFE',
#                  font=("MS Sans Serif", 76), anchor='nw')
# wid.create_button_place(frame=App.get_canvas(), image='button1.gif', command=browseFiles, x=332, y=370)
# wid1.create_button_place(frame=App.get_canvas(), image='OneEmotion.gif', command=browseFiles, x=650, y=370)
# wid2.create_button_place(frame=App.get_canvas(), image='Exit.gif', command=App.destroy, x=1050, y=600)
#App.mainloop()