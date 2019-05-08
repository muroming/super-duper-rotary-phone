import os
import uuid
from threading import Thread

import cv2
from Client.ClientThreadCallbacks import ClientThreadResponse

token_connections = 3  # How many tries to connect to socket via token
image_chunk_size = 1024
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
            print("ClientThread: ClNew file")
            current_file = os.path.join(".",
                                        cache_folder, "%s.jpg" % str(uuid.uuid4()))
            image = open(current_file, 'wb')
            while True:
                data = self.client_socket.recv(image_chunk_size)
                print("Data length:", len(data))
                if len(data) > 0:
                    image.write(data)

                if len(data) < image_chunk_size:
                    break

            image.close()
            img = cv2.imread(current_file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            socket_status = self.image_callback(
                img, self.client_socket, **self.callback_args)
            print(socket_status)
            os.remove(current_file)

        print("ClientThread: Done")
