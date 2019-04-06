from threading import Thread

token_connections = 3  # How many tries to connect to socket via token
image_chunk_size = 1024


class ClientThread(Thread):
    def __init__(self, server_socket, token, token_size=1024):
        Thread.__init__(self)
        self.server_socket = server_socket
        self.expected_token = token
        self.token_size = token_size
        self.start()

    def run(self):
        print("Started handler for:", self.server_socket)
        self.client_socket, address = self.server_socket.accept()

        connection_tries = 0
        is_connected = False
        while connection_tries < token_connections and not is_connected:
            print("Waiting token")
            received_token = self.client_socket.recv(self.token_size).decode()
            connection_tries += 1

            print(received_token)
            is_connected = received_token == self.expected_token
            if connection_tries == token_connections and not is_connected:
                return

        print("Connected")

        print("Started receiving")
        with open("test_file.jpg", 'wb') as f:
            while True:
                data = self.client_socket.recv(image_chunk_size)
                print("Data length:", len(data))
                if len(data) > 0:
                    f.write(data)
                else:
                    break

        self.stop_connection()
        print("Done")

    def stop_connection(self):
        self.client_socket.close()
        self.server_socket.close()
