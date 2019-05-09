import os
import random

import face_recognition
import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import BatchNormalization, Dense, Input
from keras.models import Sequential
from keras.models import load_model as lm

import cv2

model = None

names = {}
person_faces_amount = 300
model_path = "./NeuralNets/FaceRecognition/fc_model.h5"
encodings_path = "./NeuralNets/FaceRecognition/encodings"
encodings_name = "%s.npy"


def load_model():
    global model
    print("Loading model")
    model = lm(model_path)
    print("Loaded")


def create_fc_model(number_persons, compiled=True):
    model = Sequential()
    model.add(Dense(512, kernel_initializer='glorot_uniform',
                    activation='relu', input_shape=(None, 128)))
    model.add(BatchNormalization())
    model.add(Dense(512, kernel_initializer='glorot_uniform', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(number_persons, activation='sigmoid'))

    model.summary()

    if compiled:
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    return model


def extract_face_from_image(image, detection_type=0):
    """
    Params:
        image - RGB 3 dim array
    Output:
        face encoding: 1-dim array (1, 128) or empty if face not found
    """
    encoding = []
    face = face_recognition.face_locations(image, detection_type)
    if (len(face) != 0):
        encoding = face_recognition.face_encodings(image, face)

    return encoding


def save_person_encodings(encodings, name):
    np.save(encodings, os.path.join(encodings_path, encodings_name % name))


def load_names():
    global names
    names = [name[:-4] for names in os.listdir(encodings_path)]


def person_id_to_bin(total, id):
    res = "0" * total
    res[id] = 1
    return res


def train_classifier():
    print("Getting encodings")
    X, y = [], []
    persons = 0
    for person in os.listdir(encodings_path):
        name = person[:-4]
        print("Encodings for %s" % name)
        enc = np.load(os.path.join(encodings_path, person))
        X = np.vstack((X, enc))
        names[persons] = name
        y.extend([persons for _ in range(enc.shape[0])])
        persons += 1

    y = list(map(person_id_to_bin, y))

    print("Getting model")
    model = create_fc_model(persons)
    callbacks = [
        ModelCheckpoint(filepath=model_path, save_best_only=True),
        EarlyStopping(patience=3)
    ]

    model.fit(X, y, validation_split=.3, epochs=10, shuffle=True)

    print("Done")


def load_encodings(path):
    global encodings
    global names
    for file in os.listdir(path):
        enc = np.load(os.path.join(path, file))
        name = path.split('.')[0]
        for e in enc:
            encodings.append(e)
            names.append(name)


def validate_person(image, detection_type=0):  # Assuming image is RGB
    if model is None:
        raise RuntimeError("No model loaded")

    faces = face_recognition.face_locations(image, detection_type)
    encoding = face_recognition.face_encodings(image, faces[0])

    predict = model.predict(encoding)

    return names[np.argmax(predict)]


load_names()

if os.path.exists(model_path):
    load_model()
