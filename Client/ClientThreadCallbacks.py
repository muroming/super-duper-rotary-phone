import datetime
import os
import uuid
from enum import Enum

import numpy as np

from Database import Database
from NeuralNets.FaceRecognition import Recognition

cache_folder = "cache"
dataset_folder = "NeuralNets/FaceRecognition/encodings"
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

    faces_path = os.path.join(cache_folder, "%s_faces.npy" % username)
    if os.path.exists(faces_path):
        user_faces = np.load(faces_path)  # Collect how many faces user has
        user_faces = np.vstack((user_faces, encoding))
        print("Currect amount of faces for user", username, "%d/%d" %
              (user_faces.shape[0], Recognition.person_faces_amount))
        np.save(faces_path, user_faces)

        if len(user_faces) == Recognition.person_faces_amount:
            os.remove(faces_path)
            np.save(os.path.join(dataset_folder, "%s.npy" % username), user_faces)
            print("Person saved!")
            return ClientThreadResponse.CLOSE_SOCKET
    else:
        np.save(faces_path, encoding)

    return ClientThreadResponse.COUNTINUE_LISTENING
