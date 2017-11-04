# -*- coding: utf-8 -*-
'''
Basic support for PowerDNS version 4.0 API

:configuration: Needs static API key and URL

    .. code-block:: yaml
        pdns.url: http://127.0.0.1:8081/servers/localhost/zones/
        pdns.api: changeme

'''
from __future__ import absolute_import
import logging
import requests
import json
import urlparse
import contextlib


log = logging.getLogger(__name__)


__virtualname__ = 'pdns'

def __virtual__():
    '''
    Return virtual name of the module.
    :return: The virtual name of the module.
    '''
    return __virtualname__

def a_record(domain, hostname=None, content=None, ttl=120, prio=0):
    '''
    create or update A record. Domain and hostname need a trailing dot.
    See: https://doc.powerdns.com/md/httpapi/README


    CLI Example:
    .. code-block:: bash
        salt '*' pdns.a_record domain=example.org. hostname=subdomain.example.org. content=1.2.3.4 ttl=3600
    '''

    payload = {
        "rrsets": [
            {
                "name": hostname,
                "type": "A",
                "ttl": ttl,
                "changetype": "REPLACE",
                "records": [
                    {
                        "content": content,
                        "disabled": False,
                        "name": hostname,
                        "type": "A",
                        "ttl": ttl
                    }
                ]
            }
        ]
    }



    pdnsapi = __salt__['config.get']('pdns.api')
    pdnsurl = __salt__['config.get']('pdns.url')
    uri = urlparse.urljoin(pdnsurl, domain)
    headers = { 'X-API-Key': pdnsapi }

    r = requests.patch(uri, data=json.dumps(payload), headers=headers)

# https://doc.powerdns.com/md/httpapi/api_spec/#rest
# you may not get back a body on RR update :(
# forcing true to get the nice and green state output
# we don't want this part printed with sys.doc, so it sits here for annoyance

    if r.status_code == 204 or r.status_code == 200:
        return True
    else:
        return False

