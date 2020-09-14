#!/usr/bin/env python
# encoding: utf-8

import logging as lg
from pywhdfs.config import WebHDFSConfig
from pywhdfs.utils.utils import HdfsError
from threading import Lock

_logger = lg.getLogger(__name__)

_glock = Lock()

class Engine(object):
    
    __instance = None
    
    @staticmethod 
    def getInstance():
        _glock.acquire()
        """ Static access method. """
        if Engine.__instance == None:
            Engine()
        _glock.release()
        return Engine.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if Engine.__instance != None:
            raise Exception("Only one instance of Engine is allowed!")
        else:
            Engine.__instance = self
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

