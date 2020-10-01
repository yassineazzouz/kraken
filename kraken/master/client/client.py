#!/usr/bin/env python
# encoding: utf-8

import abc
import logging as lg

from thrift.protocol import TBinaryProtocol

# Thrift files
from thrift.transport import TSocket
from thrift.transport import TTransport

import six

from ...common.model.job import JobStatus
from ...common.model.worker import Worker
from ..thrift import MasterUserService
from ..thrift import MasterWorkerService
from ..thrift import ttypes

_logger = lg.getLogger(__name__)

WORKER_SERVICE_CLIENT_NAME = "worker-service"
USER_SERVICE_CLIENT_NAME = "user-service"


@six.add_metaclass(abc.ABCMeta)
class UserServiceClientIFace(object):
    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def list_jobs(self):
        pass

    @abc.abstractmethod
    def job_status(self, jid):
        pass

    @abc.abstractmethod
    def submit_job(self, job):
        pass

    @abc.abstractmethod
    def stop(self):
        pass


class ThriftUserServiceClient(UserServiceClientIFace):
    def __init__(self, master_host, master_port):
        self.master_host = master_host
        self.master_port = master_port

    def start(self):
        # Init thrift connection and protocol handlers
        socket = TSocket.TSocket(self.master_host, self.master_port)
        self.transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        # Set client to our Example
        self.client = MasterUserService.Client(protocol)

        # Connect to server
        self.transport.open()

    def list_jobs(self):
        jobs = []
        for job in self.client.list_jobs():
            jobs.append(
                JobStatus(
                    job.id,
                    ttypes.JobState._VALUES_TO_NAMES[job.state],
                    job.submission_time,
                    job.start_time,
                    job.finish_time,
                    job.execution_time,
                )
            )
        return jobs

    def job_status(self, jid):
        try:
            st = self.client.job_status(jid)
            return JobStatus(
                st.id,
                ttypes.JobState._VALUES_TO_NAMES[st.state],
                st.submission_time,
                st.start_time,
                st.finish_time,
                st.execution_time,
            )
        except ttypes.JobNotFoundException:
            return None

    def submit_job(self, job):
        _logger.info("Submitting new job.")
        job = ttypes.Job(job.etype, job.params)
        jid = self.client.submit_job(job)
        _logger.info("Job submitted : %s.", jid)
        return jid

    def stop(self):
        self.transport.close()


class LocalUserServiceClient(UserServiceClientIFace):
    def __init__(self, master):
        self.master = master

    def start(self):
        # do nothing
        return

    def list_jobs(self):
        return self.master.list_jobs()

    def job_status(self, jid):
        return self.master.get_job(jid)

    def submit_job(self, job):
        return self.master.submit_job()

    def stop(self):
        # do nothing
        return


@six.add_metaclass(abc.ABCMeta)
class WorkerServiceClientIFace(object):
    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def list_workers(self):
        pass

    @abc.abstractmethod
    def register_worker(self, wid, address, port):
        pass

    @abc.abstractmethod
    def unregister_worker(self, wid, address, port):
        pass

    @abc.abstractmethod
    def register_heartbeat(self, wid, address, port):
        pass

    @abc.abstractmethod
    def task_start(self, tid):
        pass

    @abc.abstractmethod
    def task_success(self, tid):
        pass

    @abc.abstractmethod
    def task_failure(self, tid):
        pass

    @abc.abstractmethod
    def stop(self):
        pass


class ThriftWorkerServiceClient(WorkerServiceClientIFace):
    """
    Worker service Thrift client.

    Used mainly by the master to to communicate with workers.
    """

    def __init__(self, master_host, master_port):
        self.master_host = master_host
        self.master_port = master_port

    def start(self):
        # Init thrift connection and protocol handlers
        socket = TSocket.TSocket(self.master_host, self.master_port)
        self.transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)

        # Set client to our Example
        self.client = MasterWorkerService.Client(protocol)

        # Connect to server
        self.transport.open()

    def list_workers(self):
        wkr_list = []
        for wkr in self.client.list_workers():
            wkr_list.append(Worker(wkr.wid, wkr.address, wkr.port))
        return wkr_list

    def register_worker(self, wid, address, port):
        return self.client.register_worker(ttypes.Worker(wid, address, port))

    def unregister_worker(self, wid, address, port):
        return self.client.unregister_worker(ttypes.Worker(wid, address, port))

    def register_heartbeat(self, wid, address, port):
        self.client.register_heartbeat(ttypes.Worker(wid, address, port))

    def task_start(self, tid):
        self.client.task_start(tid)

    def task_success(self, tid):
        self.client.task_success(tid)

    def task_failure(self, tid):
        self.client.task_failure(tid)

    def stop(self):
        self.transport.close()


class LocalWorkerServiceClient(WorkerServiceClientIFace):
    """Used by local clients accessing the master worker services directly."""

    def __init__(self, master):
        self.master = master

    def start(self):
        # do nothing
        return

    def list_workers(self):
        return self.master.list_workers()

    def register_worker(self, wid, address, port):
        self.master.register_worker(Worker(self, wid, address, port))

    def unregister_worker(self, wid, address, port):
        self.master.unregister_worker(Worker(self, wid, address, port))

    def register_heartbeat(self, wid, address, port):
        self.master.register_heartbeat(Worker(self, wid, address, port))

    def task_start(self, tid):
        self.master.task_start(tid)

    def task_success(self, tid):
        self.master.task_success(tid)

    def task_failure(self, tid):
        self.master.task_failure(tid)

    def stop(self):
        # do nothing
        return


class ClientType:
    USER_SERVICE = 1
    WORKER_SERVICE = 2

    _VALUES_TO_NAMES = {
        1: "USER_SERVICE",
        2: "WORKER_SERVICE",
    }

    _NAMES_TO_VALUES = {
        "USER_SERVICE": 1,
        "WORKER_SERVICE": 2,
    }


class LocalClientFactory(object):
    def __init__(self, master):
        self.master = master

    def create_client(self, client_type):
        if client_type == ClientType.WORKER_SERVICE:
            return LocalWorkerServiceClient(self.master)

        elif client_type == ClientType.USER_SERVICE:
            return LocalUserServiceClient(self.master)
        else:
            raise NoSuchClientException(
                "No such client [ %s ]", ClientType._VALUES_TO_NAMES[client_type]
            )


class ThriftClientFactory(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def create_client(self, client_type):
        if client_type == ClientType.WORKER_SERVICE:
            return ThriftWorkerServiceClient(self.host, self.port)

        elif client_type == ClientType.USER_SERVICE:
            return ThriftUserServiceClient(self.host, self.port)
        else:
            raise NoSuchClientException(
                "No such client [ %s ]", ClientType._VALUES_TO_NAMES[client_type]
            )


class NoSuchClientException(Exception):
    pass
