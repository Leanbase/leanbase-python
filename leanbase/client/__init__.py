import threading
import logging

from leanbase.exceptions import BadConfigurationException
from leanbase.models.config import LBClientConfig
from leanbase.storage.inmemory import SegmentStore, FeatureStore
from leanbase.tasks.workers import SegmentSyncWorker, ConveyEventsWorker


class LBClient(object):
    """ Given a message sources, processes the messages in order, populates and
    updates segment and feature stores. """ 

    def __init__(
            self,
            config:LBClientConfig=None,
            segment_store:SegmentStore=None,
            feature_store:FeatureStore=None,
        ):
        if config == None:
            raise BadConfigurationException("LB Client should be initialized with a configuration")
        self._config = config

        self._segment_store = segment_store
        self._feature_store = feature_store
        self._engage()

    def _engage(self):
        threads = []

        t = SegmentSyncWorker(self._config, self._segment_store)
        segment_sync_t = threading.Thread(name='segment-sync', target=t.start)
        segment_sync_t.start()
        threads.append(segment_sync_t)

        t = ConveyEventsWorker(self._config)
        convey_events_t = threading.Thread(name='convey-sse', target=t.start)
        convey_events_t.start()
        threads.append(convey_events_t)

        for t in threads:
            t.join()



