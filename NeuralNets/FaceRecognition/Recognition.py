import os
from threading import Thread

import face_recognition
import numpy as np
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import BatchNormalization, Dense
from keras.models import Sequential
from keras.models import load_model as lm
from keras.utils import to_categorical

import cv2

model = None
face_detector = None

names = {}
person_faces_amount = 10
model_path = "./NeuralNets/FaceRecognition/fc_model.h5"
encodings_path = "./NeuralNets/FaceRecognition/encodings"
face_cv_path = "./NeuralNets/FaceRecognition/%s"
encodings_name = "%s.npy"


class TrainingThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        print("Starting training thread")
        self.run()

    def run(self):
        train_classifier()


def load_model():
    global model
    print("Loading model")
    model = lm(model_path)
    print("Loaded")


def create_fc_model(number_persons, compiled=True):
    model = Sequential()
    model.add(Dense(512, kernel_initializer='glorot_uniform',
                    activation='relu', input_shape=(128,)))
    model.add(BatchNormalization())
    model.add(Dense(512, kernel_initializer='glorot_uniform', activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(number_persons, activation='sigmoid'))

    model.summary()

    if compiled:
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    return model


def extract_face_from_image(image):
    cv_enc = _extract_face_from_image_cv(image)
    if len(cv_enc) != 0:
        cv_enc = cv_enc[0]
    else:
        cv_enc = np.zeros((128,))
    stock_enc = _extract_face_from_image_stock(image)
    if len(stock_enc) != 0:
        stock_enc = stock_enc[0]
    else:
        stock_enc = np.zeros((128, ))

    result_enc = np.add(cv_enc, stock_enc) / (len(cv_enc) + len(stock_enc))

    return result_enc if np.any(result_enc != 0.0) else []


def _extract_face_from_image_cv(image):
    global face_detector
    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    if face_detector is None:
        face_detector = cv2.CascadeClassifier(face_cv_path % '/haarcascade_frontalface_alt.xml')

    faces = face_detector.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
    encoding = []

    if len(faces) != 0:
        faces = list(map(lambda x: (x[1], x[0] + x[2], x[1] + x[3], x[1]), faces))
        encoding = face_recognition.face_encodings(image, faces)

    return encoding


def _extract_face_from_image_stock(image, detection_type=0):
    """
    Params:
        image - RGB 3 dim array
    Output:
        face encoding: 1-dim array (1, 128) or empty if face not found
    """
    encoding = []
    face = face_recognition.face_locations(image, detection_type)
    if len(face) != 0:  # top, right, bottom, left
        encoding = face_recognition.face_encodings(image, face)

    return encoding


def save_person_encodings(encodings, name):
    np.save(encodings, os.path.join(encodings_path, encodings_name % name))


def load_names():
    global names
    names = [name[:-4] for name in os.listdir(encodings_path)]
    print(names)


def person_id_to_bin(total, id):
    res = np.zeros(total)
    res[id] = 1
    return res[0]


def train_classifier():
    print("Loading names")
    load_names()

    print("Getting encodings")
    X, y = [], []
    persons = 0
    for person in os.listdir(encodings_path):
        name = person[:-4]
        print("Encodings for %s" % name)
        enc = np.load(os.path.join(encodings_path, person))
        if len(X) != 0:
            X = np.vstack((X, enc))
        else:
            X = enc
        names[persons] = name
        y.extend([persons for _ in range(enc.shape[0])])
        persons += 1

    print("Preparing targets")
    y_bin = to_categorical(y)
    print(y_bin)

    print("Getting model")
    model = create_fc_model(persons)
    callbacks = [
        ModelCheckpoint(filepath=model_path, save_best_only=True),
        EarlyStopping(patience=3)
    ]

    model.fit(X, y_bin, validation_split=.3, epochs=10, shuffle=True, callbacks=callbacks)

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
