
Kraken
==================================


Kraken is a distributed, fast, and reliable data transfer service for efficiently moving large amounts of data between different storage technologies. It uses a distributed master worker architecture, to allow very fast data transfer speed and horizontal scaling, while implementing multiple failover, recovery and data consistency checks mechanisms to ensure robustness, fault tolerance and reliability.


*Kraken* typical use cases include but are not limited to :
- Data migration (across storage technologies)
- Data Replication.
- Backup and Disaster recovery.
- Data life cycle management.


Features
--------

* Distributed data transfer service.
* Support multiple storage technologies.
* Easy to setup, configurable services.
* Command line interface to submit and monitor jobs.
* Support multiple scheduling algorithms and job priority.
* Support multiple jobs placement policies across workers.

Install
---------------

```bash
  $ pip install kraken
```