
from ..thrift import WorkerService
from ..thrift.ttypes import Task
from ...common.model.worker import WorkerStatus

# Thrift files
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class WorkerClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        # Init thrift connection and protocol handlers
        socket = TSocket.TSocket( host , port)
        self.transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        
        # Set client to our Example
        self.client = WorkerService.Client(protocol)
        
    def start(self):
        # Connect to server
        self.transport.open()
    
    def submit(self, tid, etype, params):
        self.client.submit(Task(tid, etype, params))
    
    def worker_status(self):
        status = self.client.worker_status()
        return WorkerStatus(
                   status.wid,
                   status.running,
                   status.pending,
                   status.available)
    
    def stop(self):
        self.transport.close()
