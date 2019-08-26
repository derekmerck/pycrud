# Functions to read in and instantiate services from yaml and json

import io
from os import PathLike
from typing import Union, TextIO, List
import yaml
import json
import attr

from .serializable import AttrSerializable as Serializable
from .exceptions import EndpointHealthException


@attr.s
class EndpointManager(object):

    files = attr.ib(factory=list,
                    type=List[Union[str, PathLike, TextIO]])    # yaml formatted files
    strings = attr.ib(factory=list,
                      type=List[str])  # json formatted strings

    ep_descs = attr.ib(init=False)     # flat endpoints
    @ep_descs.default
    def load_ep_descs(self):
        ep_descs = {}
        for _file in self.files:
            if isinstance(_file, io.StringIO):
                ep_descs.update(yaml.load(f))
            elif isinstance(_file, str) or isinstance(_file, PathLike):
                with open(_file) as f:
                    ep_descs.update(yaml.load(f))
        for s in self.strings:
            ep_descs.update(json.loads(s))
        return ep_descs

    def get(self, key, check=False):
        v = self.ep_descs[key]
        ep = Serializable.Factory.create(**v)

        if check and not ep.check():
            raise EndpointHealthException(ep)

        return ep

    # "service_descs" aliases for compatibility
    service_descs = ep_descs
