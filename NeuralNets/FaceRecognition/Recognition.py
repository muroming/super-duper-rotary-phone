import os
from threading import Thread

import face_recognition
import numpy as np

import cv2
from NeuralNets.FaceRecognition.Net import BayesianModel

model = None
x_placeholder = None
model_probs = None
face_detector = None

names = []
person_faces_amount = 300
n_iters = 500
predict_threshold = 0.42
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
        try:
            train_classifier()
        except Exception as e:
            print("Training failed with exception")
            print(e)


def load_model():
    global model
    model = BayesianModel([None, 128], [None], len(names), predict_threshold,
                          n_iter_predict=n_iters, model_path=model_path, label_names=names)
    print("Model created")


def train_model(number_persons, X_data, y_data):
    model.fit(X_data, y_data)


def extract_face_from_image(image, mean_enc=False):
    """
    If mean_enc True then each face get own encoding and result is calculated as mean
    else face boundaries counted as mean
    """
    cv_face = _extract_face_from_image_cv(image)
    stock_face = _extract_face_from_image_stock(image)
    if mean_enc:
        cv_enc = get_encodings_from_image_face(
            image, cv_face) if np.any(cv_face != 0) else np.zeros((128,))
        stock_enc = get_encodings_from_image_face(
            image, stock_face) if np.any(stock_face != 0) else np.zeros((128,))
        result_enc = np.add(cv_enc, stock_enc)
        norm = np.sum([np.any(cv_enc != 0), np.any(stock_enc != 0)])
        result_enc = result_enc / norm if norm != 0 else result_enc
    else:
        mean_face = np.add(cv_face, stock_face)
        norm = np.sum([np.any(cv_face != 0), np.any(stock_face != 0)])
        mean_face = mean_face / norm if norm != 0 else mean_face
        mean_face = mean_face.astype(int)

        result_enc = get_encodings_from_image_face(
            image, mean_face) if np.any(mean_face != 0.0) else np.zeros((128,))

    return result_enc if np.any(result_enc != 0.0) else []


def get_encodings_from_image_face(image, face):
    return face_recognition.face_encodings(image, tuple(face))


def _extract_face_from_image_stock(image, detection_type=0):
    faces = face_recognition.face_locations(image, detection_type)
    return faces if len(faces) != 0 else np.zeros((4,))


def _extract_face_from_image_cv(image):
    global face_detector
    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    if face_detector is None:
        face_detector = cv2.CascadeClassifier(face_cv_path % '/haarcascade_frontalface_alt.xml')

    faces = face_detector.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
    if len(faces) > 1:
        faces = faces[0]

    try:
        return list(map(lambda x: (x[1], x[0] + x[2], x[1] + x[3], x[1]), faces)) if len(faces) != 0 else np.zeros((4,))
    except IndexError:
        print("Index error faces CV", faces, type(faces))
        return np.zeros((4,))


def save_person_encodings(encodings, name):
    np.save(encodings, os.path.join(encodings_path, encodings_name % name))


def load_names():
    global names
    names = [name[:-4] for name in os.listdir(encodings_path)]
    print("Names loaded", names)


def person_id_to_bin(y):
    unique, counts = np.unique(y, return_counts=True)
    res = []
    for u, c in zip(unique, counts):
        res.append(np.ones(c, dtype=np.int32) * u)

    return np.concatenate(np.array(res), axis=0)


def train_classifier():
    print("Loading names")
    load_names()

    if len(names) <= 1:
        print("Can't train on %d person" % len(names))
        return

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
    y_bin = person_id_to_bin(y)

    print("Training model")
    train_model(persons, X, y_bin)


def validate_person(image, detection_type=0):  # Assuming image is RGB
    if model is None:
        load_model()

    encoding = extract_face_from_image(image)

    if len(encoding) == 0:
        print("Face not found")
        return ""
    encoding = np.array(encoding[0]).reshape((1, 128))

    print(encoding.shape)
    predict = model.predict(encoding)

    return predict


load_names()
load_model()

train_classifier()
nik = np.load("./NeuralNets/FaceRecognition/encodings/nik.npy")
sh = np.load("./NeuralNets/FaceRecognition/encodings/shamil10031.npy")
ta = np.load("./NeuralNets/FaceRecognition/encodings/tanya.npy")


model.predict(ta[2].reshape((1, 128)))

obama = cv2.imread("./NeuralNets/FaceRecognition/test_obama.jpeg")
obama = cv2.cvtColor(obama, cv2.COLOR_BGR2RGB)
enc = np.array(extract_face_from_image(obama))

model.predict(enc.reshape((1, 128)))
