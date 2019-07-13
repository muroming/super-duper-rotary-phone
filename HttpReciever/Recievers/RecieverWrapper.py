import MainReciever
import Reciever


class RecieverWrapper():

    def __init__(self):
        self.recievers = [
            MainReciever()
        ]

    def init(self, is_debug):
        for reciever in self.recievers:
            if reciever is not Reciever:
                raise TypeError(reciever, "does not implement Reciever class")

            reciever.start_reciver(is_debug)

    def stop(self):
        for reciever in self.recievers:
            if reciever is not Reciever:
                raise TypeError(reciever, "does not implement Reciever class")

            reciever.stop_reciever()
