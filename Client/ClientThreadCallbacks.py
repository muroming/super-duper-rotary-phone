import os
import uuid
from enum import Enum

import numpy as np

from NeuralNets.FaceRecognition.Recognition import *

cache_folder = "cache"
dataset_folder = "./NeuralNets/FaceRecognition/encodings"


class ClientThreadResponse(Enum):
    CLOSE_SOCKET = 0
    COUNTINUE_LISTENING = 1


def add_user_photo_callback(image, username):
    """
    Params:
        image - RGB 3 dim array
    Output:
        response: AddUserResponse
    """
    encoding = extract_face_from_image(image)
    if len(encoding) == 0:
        print("Face not found!")
        return ClientThreadResponse.COUNTINUE_LISTENING

    print("Face found!")
    filename = "%s_%s.npy" % (username, str(uuid.uuid4()))
    np.save(os.path.join(cache_folder, filename), encoding)

    user_faces = list(
        filter(lambda x: username in x, os.listdir(cache_folder)))
    if len(user_faces) == person_faces_amount:
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
