import pytest

from kraken.common.model.execution_type import ExecutionType
from kraken.common.model.job import Job

from ..utils.tutils import wait_until


@pytest.mark.usefixtures("master_server")
class TestMasterService:
    def test_server_up(self, user_client):
        assert len(user_client.list_jobs()) >= 0

    def test_register_local_worker(self, worker_client):
        worker_client.register_worker("local-worker", None, None)
        assert len(worker_client.list_workers()) == 1

    def test_submit_job(self, user_client):
        jid = user_client.submit_job(Job(ExecutionType.MOCK, {"num_tasks": "10"}))
        # wait for the job to finish
        assert wait_until(
            lambda i: user_client.job_status(i).state == "FINISHED",
            20,
            0.5,
            jid,
        )

    def test_list_jobs(self, user_client):
        assert len(user_client.list_jobs()) >= 1

    def test_unregister_local_worker(self, worker_client):
        worker_client.unregister_worker("local-worker", None, None)
        assert len(worker_client.list_workers()) == 0
