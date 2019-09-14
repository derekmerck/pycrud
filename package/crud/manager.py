# Functions to read in and instantiate services from yaml and json

import io
import os
from os import PathLike
from typing import Union, TextIO, List
import yaml
import json
import attr

from .abc.serializable import AttrSerializable as Serializable
from .abc.exceptions import EndpointHealthException


@attr.s
class EndpointManager(object):

    file = attr.ib(default=None,
                   type=[Union[str, PathLike, TextIO]])    # yaml formatted files
    json = attr.ib(default=None,
                   type=str)  # json formatted strings
    yaml = attr.ib(default=None,
                   type=str)  # yaml formatted strings

    ep_descs = attr.ib(init=False)     # flat endpoints
    @ep_descs.default
    def load_ep_descs(self):
        ep_descs = {}
        if self.file:

            def load_descs(filelike):
                s = filelike.read()
                s = os.path.expandvars(s)
                ep_descs.update(yaml.load(s))

            if isinstance(self.file, io.StringIO) or isinstance(self.file, io.FileIO):
                load_descs(self.file)
            elif isinstance(self.file, str) or isinstance(self.file, PathLike):
                with open(self.file) as f:
                    load_descs(f)
        if self.json:
            _json = os.path.expandvars(self.json)
            ep_descs.update(json.loads(_json))
        if self.yaml:
            _yaml = os.path.expandvars(self.yaml)
            ep_descs.update(yaml.load(_yaml))
        return ep_descs

    def get(self, key, check=False):
        v = self.ep_descs[key]
        ep = Serializable.Factory.create(name=key, **v)

        if check and not ep.check():
            raise EndpointHealthException(ep)

        return ep

    def get_all(self, check=False):
        for k, v in self.ep_descs.items():
            if hasattr(v, "get") and v.get("ctype"):
                yield self.get(k, check=check)

    # "service_descs" aliases for compatibility
    service_descs = ep_descs
