from leanbase import exceptions
from leanbase.models.config import build_config
from leanbase.client import LBClient
from leanbase.storage import SegmentStore

_configuration = None
_client = None

def configure(api_key=None, **kwargs):
    """ Configure the leanbase client. Within a runtime, this should only be
    done once. Attempting to do this multiple times will throw an exception.
    Calling configure sets about a chain of actions:
    1. create the worker threads, and queues
    2. setup a connection with the convey endpoint, download the first set of 
       segment/feature definitions

    Internally, the configuration object is passed to all worker threads. This 
    is an immutable object and is thread safe.

    :param api_key: The API key supplied to you via https://app.leanbase.io/
    :type api_key: str

    :param **kwargs: any additional options you would like to pass. Refer docs
                     for details
    :type **kwargs: variadic keyword arguments

    :rtype: None
    """
    global _configuration, _client
    if not _configuration == None:
        raise exceptions.ReconfigurationException
    
    _configuration = build_config(api_key=api_key, **kwargs)

    _client = LBClient(
        config=_configuration,
        segment_store=SegmentStore(),
        feature_store=None
    )

def await_initialisation(timeout=1.0):
    pass

def user(user_ref):
    pass