import datetime
import os
import uuid
from enum import Enum

import numpy as np

from Database import Database
from NeuralNets.FaceRecognition import Recognition

cache_folder = "cache"
dataset_folder = "./NeuralNets/FaceRecognition/encodings"
trash_symbol = "^"


class ClientThreadResponse(Enum):
    CLOSE_SOCKET = 0
    COUNTINUE_LISTENING = 1


def authorize_user(image, socket):
    name = Recognition.validate_person(image)
    if name == "unknown" or len(name) == 0:
        name = "UNF"  # User Not Found
        result = ClientThreadResponse.COUNTINUE_LISTENING
    else:
        Database.insert_user_action(name, "AUTHORIZED WITH FACE",
                                    datetime.datetime.now())
        result = ClientThreadResponse.CLOSE_SOCKET
    print("Authorized user:", name)
    socket.send(name.encode())
    return result


def add_user_photo_callback(image, socket, username):
    """
    Params:
        image - RGB 3 dim array
    Output:
        response: AddUserResponse
    """
    encoding = Recognition.extract_face_from_image(image)
    if len(encoding) == 0:
        print("Face not found!")
        socker.send(b"NO")  # Face Not Found
        return ClientThreadResponse.COUNTINUE_LISTENING

    print("Face found!")
    socket.send(b"OK")  # Face found

    faces_path = os.path.join(cache_folder, "%s_faces.npy")
    if os.path.exists(faces_path):
        user_faces = np.load(faces_path)  # Collect how many faces user has
        if len(user_faces) == Recognition.person_faces_amount:
            user_dataset = []
            for user_face in user_faces:
                user_dataset.append(np.load(os.path.join(cache_folder, user_face)))

            user_dataset_np = np.vstack(user_dataset)
            np.save(os.path.join(dataset_folder, username), user_dataset_np)

            for user_face in user_faces:
                os.remove(os.path.join(cache_folder, user_face))

            print("Person saved!")
            return ClientThreadResponse.CLOSE_SOCKET

        return ClientThreadResponse.CLOSE_SOCKET
    else:
        np.save(faces_path, encoding)
        return ClientThreadResponse.COUNTINUE_LISTENING
