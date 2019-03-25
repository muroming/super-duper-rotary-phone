import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def getFramesFromVideo(path, size=(200, 200)):
    if type(size) is not tuple:
        raise ValueError("size is type %s not tuple" % type(size))

    video = cv2.VideoCapture(path)
    images = []
    success, image = video.read()
    while success:
        image = cv2.resize(image, size)
        images.append(image / 255.)
        success, image = video.read()

    return np.array(images, dtype=np.float32)


def saveVideoToTrain(cls, path):
    vid = cv2.VideoCapture(path)
    s = True
    ind = len(os.listdir('./FakeRecognition/TrainData/%s' % cls))
    while s:
        s, f = vid.read()
        ind += 1
        if s:
            plt.imsave('./FakeRecognition/TrainData/%s/%i.jpg' % (cls, ind), f)


saveVideoToTrain('Fake', './FakeRecognition/TrainData/Fake1.mp4')
