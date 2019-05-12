import base64
import os
import uuid
from threading import Thread

import Constants
import cv2
from Client.ClientThreadCallbacks import (ClientThreadResponse,
                                          add_user_photo_callback)
from NeuralNets.FaceRecognition.Recognition import person_faces_amount
from StringUtils import remove_string_fillers

cache_folder = "cache"


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
            data = ""
            while len(data) != img_size:
                data += self.client_socket.recv(img_size).decode()

            data = base64.b64decode(data)
            image.write(data)
            image.close()
            print("Photo num:", person_faces_amount - photos_to_recieve)
            photos_to_recieve -= 1

            img = cv2.imread(current_file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # TODO: pass save parameter
            if self.image_callback.__name__ == add_user_photo_callback.__name__:
                self.callback_args["photos"] = photos_to_recieve
            socket_status = self.image_callback(img, self.client_socket, **self.callback_args)
            os.remove(current_file)

        if os.path.exists(current_file):
            os.remove(current_file)

        self.client_socket.send(Constants.successful_response.encode())
        print("ClientThread: Done")
