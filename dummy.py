import base64
import os
import random
import socket as sk
import uuid

import matplotlib.pyplot as plt
import numpy as np

import cv2
from NeuralNets.FaceRecognition.Recognition import extract_face_from_image
from Server import serversocket_port

dataset_path = "/home/muroming/PythonProjects/SmartHouse/NeuralNets/FaceRecognition/dataset"


def login_user_test(s):
    s.send(b"0")
    s.send(fill_string("testuser testpassword", 1024).encode())
    print("All sent")
    print(s.recv(1024).decode())


def create_user_test(s):
    s.send(fill_string("2", 1024).encode())
    s.send(fill_string("testname testuser testpassword", 1024).encode())
    print("All sent")
    print(s.recv(1024).decode())


def send_pic_test(s, username):
    s.send(fill_string("4", 1024).encode())
    s.send(fill_string(username, 1024).encode())
    faces = int(s.recv(2).decode())
    print("Faces requiered:", faces)
    for _ in range(10):
        name = "no" + username + ".jpg" if _ % 2 == 0 else username + ".jpg"
        print(name)
        with open(name, 'rb') as f:
            b64 = base64.b64encode(f.read())
            s.send(fill_string(str(len(b64)), 1024).encode())
            s.send(b64)


def authorize_user_test(s):
    s.send(b"3")
    cap = cv2.VideoCapture(0)
    response = "UNF"
    while response == "UNF":
        # Capture frame-by-frame
        ret, frame = cap.read()

        filename = './cache/%s.jpg' % str(uuid.uuid4())
        cv2.imwrite(filename, frame)
        with open(filename, 'rb') as f:
            bytes = f.read()
            current_chunk = 0
            while current_chunk < len(bytes) // image_chunk_size:
                data = bytes[current_chunk *
                             image_chunk_size:(current_chunk + 1) * image_chunk_size]
                print("Bytes sent:", len(bytes))
                s.send(data)
                current_chunk += 1

            print("Last chunk")
            data = bytes[current_chunk * image_chunk_size:]
            print("Bytes sent:", len(bytes))
            s.send(data)

        os.remove(filename)
        response = s.recv(1024).decode()

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def fill_string(data, length):
    return data + "^" * (length - len(data))


def create_user_dataset(n_photos, user_name):
    saved = 0
    cap = cv2.VideoCapture(0)
    os.mkdir(os.path.join(dataset_path, user_name))
    while saved < n_photos:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face = extract_face_from_image(frame)
        if face is not None:
            cols, rows, ch = face.shape

            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), random.randint(-20, 20), 1)

            plt.imsave(os.path.join(dataset_path, user_name, user_name + str(saved) + ".jpg"), face)
            plt.imsave(os.path.join(dataset_path, user_name, user_name + str(saved) + "rot.jpg"),
                       cv2.warpAffine(face, M, (cols, rows)))

            saved += 1


# s=sk.socket(sk.AF_INET, sk.SOCK_STREAM)
# s.connect(("127.0.0.1", serversocket_port))
#
# send_pic_test(s, "ka")
create_user_dataset(5, "sha")

# saved = 0
# for mock in os.listdir("/home/muroming/PythonProjects/SmartHouse/NeuralNets/FaceRecognition/dataset/mock/"):
#     print(mock)
#     img = cv2.imread(
#         "/home/muroming/PythonProjects/SmartHouse/NeuralNets/FaceRecognition/dataset/mock/" + mock)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     face = extract_face_from_image(img)
#     if face is not None:
#         cols, rows, ch = face.shape
#
#         M = cv2.getRotationMatrix2D((cols / 2, rows / 2), random.randint(-20, 20), 1)
#
#         plt.imsave("/home/muroming/PythonProjects/SmartHouse/NeuralNets/FaceRecognition/dataset/mock/" +
#                    mock + str(saved) + ".jpg", face)
#         plt.imsave("/home/muroming/PythonProjects/SmartHouse/NeuralNets/FaceRecognition/dataset/mock/" +
#                    mock + str(saved) + "rot.jpg", cv2.warpAffine(face, M, (cols, rows)))
#         os.remove("/home/muroming/PythonProjects/SmartHouse/NeuralNets/FaceRecognition/dataset/mock/" + mock)
#
#         saved += 1
#         print(saved)
