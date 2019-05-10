import base64
import os
import uuid
from threading import Thread

import cv2
from Client.ClientThreadCallbacks import ClientThreadResponse
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
                print("Recieving more")
                data += self.client_socket.recv(img_size).decode()

            print(data, len(data))
            data = base64.b64decode(data)
            image.write(data)
            image.close()
            img = cv2.imread(current_file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            socket_status = self.image_callback(
                img, self.client_socket, **self.callback_args)
            print(socket_status)
            os.remove(current_file)

        print("ClientThread: Done")
