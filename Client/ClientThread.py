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
        self.is_running = False
        self.start()

    def run(self):
        self.is_running = True
        print("Started receiving")
        result = ClientThreadResponse.COUNTINUE_LISTENING
        current_file = ""
        while result == ClientThreadResponse.COUNTINUE_LISTENING:
            current_file = os.path.join(cache_folder, "%s.jpg" % str(uuid.uuid4()))
            image = open(current_file, 'wb')
            while True:
                data = self.client_socket.recv(image_chunk_size)
                print("Data length:", len(data))
                image.write(data)

                if len(data) < image_chunk_size:
                    break

            image.close()
            img = cv2.imread(current_file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = self.image_callback(img, **self.callback_args)

            os.remove(current_file)

        self.stop_connection()
        print("Done")

    def stop_connection(self):
        self.is_running = False
