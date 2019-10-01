from collections import namedtuple
from leanbase import exceptions

_config_keys = [
    'api_key',
    'convey_host'
]

LBClientConfig = namedtuple("LBClientConfig", _config_keys)

class _LBClientConfig(object):
    def __init__(self, api_key=None, **kwargs):
        if api_key is None:
            raise exceptions.BadConfigurationException('api_key cannot be None')

        # First, we set the defaults
        self.convey_host = 'https://convey.leanbase.io/'

        # Now, if any overrides have been passed, we override them.
        for (k, v) in kwargs.iteritems():
            if k in _config_keys:
                setattr(self, k, v)
            else:
                raise exceptions.BadConfigurationException('provided key: {} is not a supported config key'.format(k))
    
def build_config(api_key=None, **kwargs):
    """ Returns namedtuple LBClientConfig after passing it through the
    intermediary class _LBClientConfig. """
    config = _LBClientConfig(api_key=api_key, **kwargs)
    return LBClientConfig(
        map(
            lambda k: getattr(config, k),
            _config_keys
        )
    )
