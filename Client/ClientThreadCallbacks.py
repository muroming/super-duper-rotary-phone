import datetime
import os
from enum import Enum

import numpy as np

import Constants
from Database import Database
from NeuralNets.FaceRecognition import Recognition
from StringUtils import fill_string

cache_folder = "cache"
dataset_folder = "NeuralNets/FaceRecognition/dataset"


class ClientThreadResponse(Enum):
    CLOSE_SOCKET = 0
    COUNTINUE_LISTENING = 1


def authorize_user(image, socket, photo_attempts):
    name = Recognition.validate_person(image)
    if len(name) == 0:
        print("User not found")
        socket.send(fill_string(Constants.error_response, 1024).encode())
        result = ClientThreadResponse.COUNTINUE_LISTENING
    else:
        print("Authorized user:", name)
        # Database.insert_user_action(name, "AUTHORIZED WITH FACE",datetime.datetime.now())
        result = ClientThreadResponse.CLOSE_SOCKET
        socket.send(fill_string(Constants.successful_response, 1024).encode())

    if photo_attempts == 0:
        result = ClientThreadResponse.CLOSE_SOCKET
    return result


def add_user_photo_callback(image, socket, username, photos):
    """
    Params:
        image - RGB 3 dim array
    Output:
        response: AddUserResponse
    """

    encoding = Recognition.extract_face_enc_from_image(image)
    faces_path = os.path.join(cache_folder, "%s_faces.npy" % username)

    if os.path.exists(faces_path):
        user_faces = np.load(faces_path)  # Collect how many faces user has

    if len(encoding) == 0:
        print("Face not found!")
        result = ClientThreadResponse.COUNTINUE_LISTENING
    else:
        print("Face found!")

        if os.path.exists(faces_path):
            user_faces = np.vstack((user_faces, encoding))
            print("Currect amount of faces for user", username, "%d/%d" %
                  (user_faces.shape[0], Recognition.person_faces_amount))
            np.save(faces_path, user_faces)
        else:
            np.save(faces_path, encoding)

        result = ClientThreadResponse.COUNTINUE_LISTENING

    if photos == 0:
        print("Trying to save person")
        if os.path.exists(faces_path):
            os.remove(faces_path)
            if not os.path.exists(os.path.join(dataset_folder, username)):
                os.mkdir(os.path.join(dataset_folder, username))
            np.save(os.path.join(dataset_folder, username, "%s.npy" % username), user_faces)
            print("Person saved!")
            Recognition.TrainingThread()
        result = ClientThreadResponse.CLOSE_SOCKET

    return result
