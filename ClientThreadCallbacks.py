import os
import uuid
from enum import Enum

import numpy as np

from NeuralNets.FaceRecognition.Recognition import extract_face_from_image


class ClientThreadResponse(Enum):
    CLOSE_SOCKET = 0
    COUNTINUE_LISTENING = 1


def add_user_callback(image, username):
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
    filename = username + str(uuid.uuid4()) + ".npy"
    np.save(os.path.join(cache_folder, filename), encoding)

    # TODO: save embeddings if gathered enough faces
    if len(list(filter(lambda x: username in x, os.listdir(cache_folder)))) == 0:
        print("Person saved!")
        return ClientThreadResponse.CLOSE_SOCKET

    return ClientThreadResponse.COUNTINUE_LISTENING
