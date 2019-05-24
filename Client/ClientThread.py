import base64
import os
import uuid
from threading import Thread

import Constants
import cv2
from Client.ClientThreadCallbacks import (ClientThreadResponse,
                                          add_user_photo_callback,
                                          authorize_user)
from NeuralNets.FaceRecognition.Recognition import person_faces_amount
from StringUtils import remove_string_fillers

cache_folder = "cache"


def safe_decode(data):
    """
    Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    if len(data) % 4 != 0:
        raise RuntimeError("Wrong padding but I got u <3")
    return base64.b64decode(data)


class ClientThread(Thread):
    def __init__(self, client_socket, image_callback, **kwargs):
        Thread.__init__(self)
        self.client_socket = client_socket
        self.image_callback = image_callback
        self.callback_args = kwargs
        self.start()

    def run(self):
        print("ClientThread: Started receiving")
        socket_status = ClientThreadResponse.COUNTINUE_LISTENING
        current_file = ""
        photos_to_recieve = person_faces_amount
        while socket_status == ClientThreadResponse.COUNTINUE_LISTENING:
            print("ClientThread: New file")

            img_size = self.client_socket.recv(1024).decode()
            img_size = remove_string_fillers(img_size)
            img_size = int(img_size)

            print("Expected img_size:", img_size)

            current_file = os.path.join(".", cache_folder, "%s.jpg" % str(uuid.uuid4()))
            image = open(current_file, 'wb')
            data = b""
            while len(data) != img_size:
                data += self.client_socket.recv(img_size - len(data))

            try:
                data = base64.b64decode(data)
                image.write(data)
            except Exception as e:
                print("Exception while decode", e)
                print(data)
                image.close()
                continue

            image.close()

            print("Photo num:", person_faces_amount - photos_to_recieve)
            photos_to_recieve -= 1

            img = cv2.imread(current_file)
            cols, rows, ch = img.shape

            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), random.randint(-20, 20), 1)
            rot_img = cv2.warpAffine(img, M, (cols, rows))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            rot_img = cv2.cvtColor(rot_img, cv2.COLOR_BGR2RGB)
            # TODO: pass save parameter
            if self.image_callback.__name__ == add_user_photo_callback.__name__:
                self.callback_args["photos"] = photos_to_recieve
            elif self.image_callback.__name__ == authorize_user.__name__:
                self.callback_args["photo_attempts"] -= 1
            img_result = self.image_callback(img, self.client_socket, **self.callback_args)
            rot_result = self.image_callback(rot_img, self.client_socket, **self.callback_args)
            socket_status = ClientThreadResponse.COUNTINUE_LISTENING if img_result == rot_result == ClientThreadResponse.COUNTINUE_LISTENING else ClientThreadResponse.CLOSE_SOCKET
            print()
        #     os.remove(current_file)
        #
        # if os.path.exists(current_file):
        #     os.remove(current_file)

        self.client_socket.send(Constants.successful_response.encode())
        print("ClientThread: Done")
