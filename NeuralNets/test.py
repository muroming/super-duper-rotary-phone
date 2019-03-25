import cv2
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense, Dropout, MaxPooling2D
import numpy as np

model = Sequential()

data = []

vidcap = cv2.VideoCapture('./test.webm')
s, f = vidcap.read()
fs = 1
f = cv2.resize(f, (300, 300)) / 255.
data.append(f)

while (fs < 1200):
    s, f = vidcap.read()
    if not s:
        break
    f = cv2.resize(f, (300, 300)) / 255.
    data.append(f)
    fs += 1

data = np.array(data, dtype=np.float32)
np.random.shuffle(data)

model.add(Conv2D(16, (3, 3), activation='relu', input_shape=(300, 300, 3)))
model.add(Conv2D(16, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.summary()
