from multiprocessing import Queue
from abc import ABC
import attr


@attr.s(cmp=False, hash=None)
class DaemonMixin(ABC):
    """
    API for Endpoints that can run
    """

    job_queue = attr.ib( init=False, factory=Queue )

    def handle_item(self, item, dryrun=False):
        raise NotImplementedError

    def handle_queue(self, dryrun=False):
        while not self.job_queue.empty():
            item = self.job_queue.get()
            self.handle_item(item, dryrun=dryrun)

    def run(self, dryrun=False):
        # Fill queue and then handle it
        raise NotImplementedError
