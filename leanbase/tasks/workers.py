import logging
import threading
from six.moves import queue

from leanbase.storage import SegmentStore, FeatureStore
from leanbase.client import lbconvey, sse
from leanbase.models.config import LBClientConfig

SEGMENT_Q = queue.Queue()
FEATURE_Q = queue.Queue()

class FeatureSyncWorker(object):
    def __init__(self, config:LBClientConfig, feature_store:FeatureStore):
        self.config = config
        self.feature_store = feature_store
        self._should_stop = False

    def start(self):
        logging.info('Thread<%s> Started', threading.current_thread().getName())
        self.initialize()

    def stop(self):
        self._should_stop = True

    def initialize(self):
        for feature_id in lbconvey.list_all_features(self.config.team_id):
            FEATURE_Q.put(feature_id)
        self.main_loop()

    def main_loop(self):
        while True:
            if self._should_stop:
                break
            
            try:
                updated_id = FEATURE_Q.get(True, 1)
                self._update_feature(feature_id=updated_id)
            except queue.Empty:
                pass

        logging.info('Thread<%s> Stopped', threading.currentThread().getName())

    def _update_feature(self, feature_id:str=None):
        status = lbconvey.get_feature_status(self.config.team_id, feature_id)
        if status:
            self.feature_store.set_feature(feature_id, status)
            logging.debug('Updated feature status for id: %s', feature_id)

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
        self._update_segment('$STAFF')
        logging.info('Populated staff segment definition')
        self.main_loop()

    def main_loop(self):
        while True:
            if self._should_stop:
                break
            
            try:
                updated_id = SEGMENT_Q.get(True, 1)
                self._update_segment(segment_id=updated_id)
            except queue.Empty:
                pass

        logging.info('Thread<%s> Stopped', threading.currentThread().getName())

    def _update_segment(self, segment_id:str=None):
        self.segment_store.set_segment(
            segment_id,
            lbconvey.get_staff_segment_definition(self.config.team_id)
        )
        logging.debug('Updated segment definition for id: %s', segment_id)

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
            if message['resource_type'] == 'segment':
                SEGMENT_Q.put(message['resource_id'])
            elif message['resource_type'] == 'feature':
                FEATURE_Q.put(message['resource_id'])

        logging.info('Thread<%s> Stopped', threading.currentThread().getName())

    