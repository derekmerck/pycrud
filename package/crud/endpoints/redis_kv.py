from typing import Union
import logging
import json
import attr
from redis import Redis as RedisHandler
from ..abc import Endpoint, Serializable, Item, ItemID


@attr.s
class RedisKV(Endpoint, Serializable):
    """
    CRUD endpoint using a redis db for persistent kv storage
    """

    url = attr.ib(default="redis://")
    db = attr.ib(default=0)
    prefix = attr.ib(default="item:")
    gateway = attr.ib(init=False)

    @gateway.default
    def set_gateway(self):
        return RedisHandler.from_url(self.url, db=self.db)

    clear = attr.ib(default=False)

    def __attrs_post_init__(self):
        if self.clear:
            self.flush()

    def flush(self):
        self.gateway.flushdb()

    def keys(self):
        keys = self.gateway.keys("{}*".format(self.prefix))
        _keys = []
        for key in keys:
            key = key.decode("utf-8")
            _keys.append(key[len(self.prefix):])
        return _keys

    def get(self, item: Union[Item, ItemID], *args, **kwargs):

        if hasattr(item, "epid"):
            item_id = item.epid
        else:
            item_id = item

        key = "{}{}".format(self.prefix, item_id).encode("utf-8")
        logging.debug(key)
        item_flat = self.gateway.get(key)
        item_dict = json.loads(item_flat)
        item = Serializable.Factory.create(**item_dict)
        return item

    def put(self, item: Item, *args, **kwargs):
        item_id = item.epid
        item_flat = item.json()
        key = "{}{}".format(self.prefix, item_id).encode("utf-8")
        self.gateway.set(key, item_flat)

    def sget(self, skey: str):

        item_ids = self.gateway.smembers(skey.encode("utf-8"))
        result = []
        for item_id in item_ids:
            result.append(self.get(item_id))
        return result

    def sput(self, item: Union[Item, ItemID], skey: str):

        self.put(item)
        if hasattr(item, "epid"):
            item_id = item.epid
        else:
            item_id = item
        self.gateway.sadd(skey.encode("utf-8"), item_id)


RedisKV.register("Redis")
