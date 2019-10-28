# Python-CRUD

Derek Merck  
<derek.merck@ufl.edu>  
University of Florida and Shands Hospital  
Gainesville, FL  

Python framework for implementing CRUD (create, retrieve, update, delete) service endpoints and management daemons.  Supports distributed task management with [celery[].

[celery]: http://www.celeryproject.org

The [Python-DIANA][] library extends Python-CRUD with DICOM-relevant items, endpoints, tasks, and daemons.

[python-diana]: http://github.com/derekmerck/diana2

The [Python-WUPHF][] library extends Python-CRUD with SMTP and SMS messenger endpoints and a dispatcher daemon.

[python-wuphf]: http://github.com/derekmerck/wuphf

## Usage

Endpoints provide an abstraction layer between application specific logic and technical implementations of specific services such a file directories or servers (generically called Gateways here).  Method syntax generally follows standard KV nomenclature (get, put, find, etc.)

Endpoints handle Items, which may include metadata, data, and other attributes.  Items may be referenced by an ItemID for Get or Delete requests.  Put requests require an Item type argument.  And Find requests describe Items by a mapping Query.

### Command-line Interface

Command-line bindings for "service-level" tasks are also provided in `crud-cli`.  Specifically, given a service description file (endpoint kwargs as yaml), an endpoint can be created and methods (get, put, etc) called on it via command-line.

## License

MIT
