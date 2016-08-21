"""
Codes are from http://lukasa.co.uk/2013/01/Choosing_SSL_Version_In_Requests/

It is used to choose a SSL version manually so that I can successfully
connect to NTU server to fetch course schedule data.

Thanks for Lukasa's work :)
"""

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class SSLAdapter(HTTPAdapter):
    """An HTTPS Transport Adapter that uses an arbitrary SSL version."""

    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version

        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=self.ssl_version)
