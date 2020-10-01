import logging as lg
from threading import Lock

from pywhdfs.config import WebHDFSConfig

_logger = lg.getLogger(__name__)

_glock = Lock()


class ClientFactory(object):
    __instance = None

    @staticmethod
    def getInstance():
        with _glock:
            """ Static access method. """
            if ClientFactory.__instance is None:
                ClientFactory()
        return ClientFactory.__instance

    def __init__(self):
        if ClientFactory.__instance is not None:
            raise Exception("Only one instance of Client Factory is allowed!")
        else:
            ClientFactory.__instance = self
            self._configure()

    def _configure(self):
        self.config = WebHDFSConfig(None)
        self.clients = {}

    def get_client(self, name):
        with _glock:
            if name in self.clients:
                client = self.clients[name]
            else:
                client = self.config.get_client(name)
                # This is an ugly workaround to initialize the client
                client.list("/")
                self.clients[name] = client
        return client
