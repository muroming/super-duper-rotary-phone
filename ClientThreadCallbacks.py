import os
import uuid
from enum import Enum

import numpy as np

from ClientThread import cache_folder
from NeuralNets.FaceRecognition.Recognition import extract_face_from_image


class AddUserResponse(Enum):
    FACE_NOT_ADDED = 0
    FACE_ADDED = 1
    USER_SAVED = 2


def add_user_callback(username, image):
    """
    Params:
        image - RGB 3 dim array
    Output:
        response: AddUserResponse
    """
    encoding = extract_face_from_image(image)
    if len(encoding) == 0:
        return AddUserResponse.FACE_NOT_ADDED

    filename = username + str(uuid.uuid4()) + ".npy"
    np.save(os.path.join(cache_folder, filename), encoding)

    # TODO: save embeddings if gathered enough faces
    if len(list(filter(lambda x: username in x, os.listdir(cache_folder)))) == 0:
        return AddUserResponse.USER_SAVED

    return AddUserResponse.FACE_ADDED
