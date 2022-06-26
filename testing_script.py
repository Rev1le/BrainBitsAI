import yolov5_face
import os
import re
import csv
import json
yolo5_face = yolov5_face.AI_Yolov5()

global path

emotions = ("angry","disgust","fear","happy","sad","surprise","neutral")


def get_path_video():
    global path
    return path



def set_path(pathFile: str):
    global path
    path = pathFile

list_name_files = []


def get_video_lenght():
    return 'short'

def list_file():
    for dirname, _, filenames in os.walk(input('Введите путь до папки с файлами')):
            list_file=[os.path.join(dirname, filename) for filename in filenames]
    return list_file

x = list()

for i in list_file():
    #сделать try
    set_path(i)
    regular = r'(([^()]+(([^)]+)[^)])).)'
    emotion_dict = yolo5_face.find_faces_from_video(path = get_path_video, video_length=get_video_lenght)
    max_emotion_num, max_emothion_precent = 0, 0.0
    for k, v in emotion_dict.items():

        try:
            precent = v[0][0].split()[1][1:-2]
            #print('эмоцииииии', precent)
            emotion_num = v[0][1]
            if float(precent) > max_emothion_precent:
                max_emotion_num, max_emothion_precent = emotion_num, precent
                # print(precent, max_emothion_precent)
            #vyr = re.search(regular, v[0][0])
            #print("резульатт регулярки",vyr.group(0))
        except Exception:
            pass

    print('Вывод ', get_path_video().split("\\")[-1], max_emotion_num)
    x.append({"filename": get_path_video().split("\\")[-1], "emotion": max_emotion_num})

#= str(x).replace("'", '"')
#print(x)
#x = json.dumps(x)

f = csv.writer(open("test.csv", "w", newline=''))

# Write CSV Header, If you dont need that, remove this line
f.writerow(["filename", "emotion"])

for x in x:
    #f.writerow([x["filename"],
    #            x["emotion"]])
    f.writerow([x["filename"],
                x["emotion"]])
