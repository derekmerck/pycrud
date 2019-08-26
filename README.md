# Python-CRUD

Derek Merck  
Brown University

`python-crud` is a framework for implementing CRUD (create, retrieve, update, delete) service endpoints and distributed task management with `python` and `celery`.

The `python-diana` library extends `python-crud` with DICOM-relevant items, endpoints, tasks, and daemons.

## Usage

Endpoints handle generic Items, which may be referenced by an ItemID for Get requests.  Put requests require an Item type argument.  Find requests describe Items by a mapping Query.

Endpoints provide an abstraction layer between application specific logic and technical implementations of 
