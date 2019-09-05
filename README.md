# Python-CRUD

Derek Merck  
University of Florida at Gainesville  
Summer 2019  

Provides a Python framework for implementing CRUD (create, retrieve, update, delete) service endpoints and distributed task management with [celery[].

[celery]: http://www.celeryproject.org

The [Python-DIANA][] library extends Python-CRUD with DICOM-relevant items, endpoints, tasks, and daemons.

[python-diana]: http://github.com/derekmerck/diana2

The [Python-WUPHF][] library extends Python-CRUD with SMTP and SMS messenger endpoints and a dispatcher daemon.

[python-wuphf]: http://github.com/derekmerck/wuphf

## Usage

Endpoints provide an abstraction layer between application specific logic and technical implementations of specific services such a file directories or servers (generically called Gateways here).  Method syntax generally follows standard KV nomenclature (get, put, find, etc.)

Endpoints handle Items, which may include metadata, data, and other attributes.  Items may be referenced by an ItemID for Get or Delete requests.  Put requests require an Item type argument.  And Find requests describe Items by a mapping Query.
