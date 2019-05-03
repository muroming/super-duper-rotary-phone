import os
import pickle


class ClientAction(object):
    def __init__(self, client, action):
        self.client = client
        self.action = action
        # TODO: self.time = date()
