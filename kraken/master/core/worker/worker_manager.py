
from .worker import RemoteThriftWorker
from threading import Thread, RLock
from datetime import datetime

import logging as lg
_logger = lg.getLogger(__name__)

class WorkerManager(object):
    '''
    The WorkerManager monitor the state of workers, and
    maintain the list of active/dead workers.
    '''
    
    def __init__(self):
        self.live_workers = []
        self.decommissioning_workers = []
        self.dead_workers = []
        
        self.lock = RLock()

    def start(self):
        _logger.info("Stating kraken worker manager.")
        self.monitor = WorkersMonitor(self)
        self.monitor.setDaemon(True)
        self.monitor.start()
        _logger.info("Kraken worker manager started.")
    
    def stop(self):
        _logger.info("Stopping kraken worker manager.")
        self.monitor.stop()
        self.monitor.join()
        _logger.info("Kraken worker manager stopped.")
        
    def get_live_worker(self, wid):
        with self.lock:
            for wkr in self.live_workers:
                if wkr.wid ==   wid:
                    return wkr
            return None
     
    def list_live_workers(self):
        with self.lock:
            return self.live_workers

    def list_decommissioning_workers(self):
        with self.lock:
            return self.decommissioning_workers
        
    def register_worker(self, worker):
        with self.lock:
            for wkr in self.live_workers:
                if (wkr.wid == worker.wid):
                    _logger.error("Worker [ %s ] is already registered.", worker.wid)
                    raise AlreadyRegisteredWorkerException("Worker [ %s ] is already registered.", worker.wid)
                elif (wkr.address == worker.address and wkr.port == worker.port):
                    _logger.error("Worker running on address [ %s ] and port [ %s ] is already registered.", worker.address, worker.port)
                    raise AlreadyRegisteredWorkerException("Worker running on address [ %s ] and port [ %s ] is already registered.", worker.address, worker.port)
                elif (wkr.address == worker.address):
                    _logger.warn("Another Worker [ %s ] is already running on [ %s ].", worker.wid, worker.address)

            for wkr in self.decommissioning_workers:
                _logger.error("Worker [ %s ] is in decommissioning state in can not be regestired.", worker.wid)
                raise AlreadyRegisteredWorkerException("Worker [ %s ] is in decommissioning state in can not be regestired.", worker.wid)
                
            remote_worker = RemoteThriftWorker(worker.wid,worker.address, worker.port)
            remote_worker.start()
            self.live_workers.append(remote_worker)

    def register_heartbeat(self, worker):
        with self.lock:
            remote_worker = self.get_live_worker(worker.wid)
            if remote_worker != None:
                remote_worker.last_hear_beat = datetime.now()
            else:
                raise NoSuchWorkerException("No such worker [ %s ]", worker.wid)
                    
    def decommission_worker(self, wid):
        _logger.info("Decommisionning Worker [ %s ]", wid)
        with self.lock:
            remote_worker = self.get_live_worker(wid)
            if remote_worker != None:
                self.live_workers.remove(remote_worker)
                self.decommissioning_workers.append(remote_worker)
            else:
                raise NoSuchWorkerException("No such worker [ %s ]", wid)
        _logger.info("Worker [ %s ] Decommisionned", wid)

    def on_worker_decommissioned(self, wid):
        _logger.info("Deleting Worker [ %s ]", wid)
        with self.lock:
            for wkr in self.decommissioning_workers:
                if(wkr.wid == wid):
                    wkr.stop()
                    self.decommissioning_workers.remove(wkr)
                    self.dead_workers.append(wkr)
                    break
        _logger.info("Worker [ %s ] Deleted", wid)

            
class WorkersMonitor(Thread):
    
    # in seconds
    heartbeat_check_interval = 30
    
    def __init__(self, manager):
        super(WorkersMonitor, self).__init__()
        self.manager = manager
        self.stopped = False
        
    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            for worker in self.manager.list_live_workers():
                if (datetime.now() - worker.last_hear_beat).total_seconds() > self.heartbeat_check_interval:
                    _logger.warn("Missing worker hearbeat from [ %s ] after %s seconds", worker.wid, self.heartbeat_check_interval)
                    self.manager.decommission_worker(worker.wid)
                

class IllegalWorkerStateException(Exception):
    pass

class NoSuchWorkerException(Exception):
    pass

class AlreadyRegisteredWorkerException(Exception):
    pass