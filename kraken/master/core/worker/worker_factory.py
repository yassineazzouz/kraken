
from .worker import RemoteThriftWorker
from ...standalone.worker import LocalWorker


class WorkerFactory(object):

    def __init__(self, master):
        self.master = master

    def create_worker(self, worker):
        if worker.address is not None and worker.port is not None:
            return RemoteThriftWorker(worker.wid, worker.address, worker.port)
        else:
            return LocalWorker(worker.wid, self.master)
