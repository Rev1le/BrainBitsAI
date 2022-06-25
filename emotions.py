import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
import cv2
from PIL import Image
#from vgg import create_RepVGG_A0 as create НЕПОНЯТКА
import numpy as np
# Load model
import time

# 8 Emotions
emotions = ("anger", "contempt", "disgust", "fear", "happy", "neutral", "sad", "surprise")


class Detector():
    def __init__(self, device):
        # Initialise model
        self.model = create(deploy=True)
        self.dev = device
        self.model.to(device)
        checkpoint = torch.load("weights/vgg.pth")
        if 'state_dict' in checkpoint:
            checkpoint = checkpoint['state_dict']
        ckpt = {k.replace('module.', ''): v for k, v in checkpoint.items()}
        self.model.load_state_dict(ckpt)

        # Change to classify only 8 features
        self.model.linear.out_features = 8
        self.model.linear._parameters["weight"] = self.model.linear._parameters["weight"][:8, :]
        self.model.linear._parameters["bias"] = self.model.linear._parameters["bias"][:8]

        # Save to eval
        cudnn.benchmark = True
        self.model.eval()

    def detect_emotion(self, images, conf=True):
        with torch.no_grad():
            # Normalise and transform images
            normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                             std=[0.229, 0.224, 0.225])
            x = torch.stack([transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                normalize,
            ])(Image.fromarray(image)) for image in images])
            # Feed through the model
            y = self.model(x.to(self.dev))
            result = []
            for i in range(y.size()[0]):
                # Add emotion to result
                emotion = (max(y[i]) == y[i]).nonzero().item()
                # Add appropriate label if required
                result.append(
                    [f"{emotions[emotion]}{f' ({100 * y[i][emotion].item():.1f}%)' if conf else ''}", emotion])
        return result

# start_time = time.time()
# im = np.array([cv2.imread("test2.jpg")])
# init('cpu')
# print(detect_emotion(im,True),"--- %s seconds ---" % (time.time() - start_time))