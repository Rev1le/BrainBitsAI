import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms
import cv2
from PIL import Image
from vgg import create_RepVGG_A0 as create
import numpy as np
# Load model
model = create(deploy=True)

# 8 Emotions
emotions = ("anger","contempt","disgust","fear","happy","neutral","sad","surprise")

def init(device):
    # Initialise model
    global dev
    dev = device
    model.to(device)
    checkpoint = torch.load("weights/vgg.pth")
    if 'state_dict' in checkpoint:
        checkpoint = checkpoint['state_dict']
    ckpt = {k.replace('module.', ''):v for k,v in checkpoint.items()}
    model.load_state_dict(ckpt)
    
    # Change to classify only 8 features
    model.linear.out_features = 8
    model.linear._parameters["weight"] = model.linear._parameters["weight"][:8,:]
    model.linear._parameters["bias"] = model.linear._parameters["bias"][:8]

    # Save to eval
    cudnn.benchmark = True
    model.eval()

def detect_emotion(images,conf=True):
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
        y = model(x.to(dev))
        result = []
        for i in range(y.size()[0]):
            # Add emotion to result
            emotion = (max(y[i]) == y[i]).nonzero().item()
            # Add appropriate label if required
            result.append([f"{emotions[emotion]}{f' ({100*y[i][emotion].item():.1f}%)' if conf else ''}",emotion])
    return result

im = np.array([cv2.imread("test.jpg")])
init('cpu')
print(detect_emotion(im,True))
