import logging
import threading

from leanbase.storage import SegmentStore
from leanbase.client import lbconvey, sse
from leanbase.models.config import LBClientConfig

class SegmentSyncWorker(object):
    def __init__(self, config:LBClientConfig, segment_store:SegmentStore):
        self.config = config
        self.segment_store = segment_store
        self._should_stop = False

    def start(self):
        logging.info('Thread<%s> Started', threading.currentThread().getName())
        self.initialize()

    def stop(self):
        self._should_stop = True

    def initialize(self):
        self.segment_store.set_segment(
            '$STAFF',
            lbconvey.get_staff_segment_definition(self.config.team_id)
        )
        logging.info('Populated staff segment definition')
        self.main_loop()

    def main_loop(self):
        while True:
            if self._should_stop:
                break

        logging.info('Thread<{}> Stopped', threading.currentThread().getName())


class ConveyEventsWorker(object):
    def __init__(self, config:LBClientConfig):
        self.config = config
        self._should_stop = False

    def start(self):
        logging.info('Thread<%s> Started', threading.currentThread().getName())
        self.initialize()

    def stop(self):
        self._should_stop = True

    def initialize(self):
        self._source = sse.SSEMessageSource(self.config)
        self.main_loop()

    def main_loop(self):
        for message in self._source:
            logging.info(message)
        # while True:
        #     if self._should_stop:
        #         break
            
        #     logging.info('Waiting for the next event')
        #     message = next(self._source)

        logging.info('Thread<%s> Stopped', threading.currentThread().getName())

    