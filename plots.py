import random
from matplotlib import pyplot as plt
import numpy as np


class plots():

    def __init__(self) -> None:
        self.all_data = []
        self.RangeDict = ["anger", "contempt", "disgust", "fear", "sad", "neutral", "surprise", "happy"]

    def create_plot(self, array_x: np.array, array_y: np.array):
        plt.plot(array_x, array_y)
        plt.ylabel(
            "anger:1,\n + \n + contempt:2, \n + \n + disgust:3, \n +  \n +fear:4, \n +  \n +sad:5, \n + \n +neutral:6, \n + \n +surprise:7, \n + \n + happy:8",
            rotation=0)

        # plt.yticks(rotation = 90)
        # plt.show()
        plt.savefig('myfig.png')

    def create_pirog(self, data: list):
        list_name_emotions = []

        if len(data) == 0:
            return

        for emotion in data:
            em = emotion[0].split()[0]
            list_name_emotions.append(em)

        fig, ax = plt.subplots()

        self.all_data += list_name_emotions
        emotions = {i: self.all_data.count(i) for i in self.RangeDict}
        ax.axis('equal')
        precent = [emotions[i] / len(emotions) for i in emotions]
        print(precent)
        print(emotions)

        list_mass = dict()
        list_list_top = []

        for ind, val in enumerate(precent):
            if val > 0 :
                list_mass[self.RangeDict[ind]] = val
                list_list_top.append(val)

        print(list_mass)

        ax.pie(list_list_top, labels=list_mass.keys(), autopct='%1.1f%%')
        fig.savefig('pie.png')

