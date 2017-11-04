# -*- coding: utf-8 -*-
'''
PowerDNS state

.. code-block:: yaml

    example.org.:
      pdns.a_record:
        - name: example.org.
        - hostname: host123.example.org.
        - content: 1.2.3.4
        - ttl: 8400

'''

# Import python libs
import os.path

# Import Salt libs
import salt.utils

from salt.exceptions import CommandExecutionError


def _error(ret, err_msg):
    ret['result'] = False
    ret['comment'] = err_msg
    return ret


def a_record(name, domain, hostname, content, ttl):

    ret = {'name': domain,
           'changes': {},
           'result': None,
           'comment': ''}

    result = __salt__['pdns.a_record'](domain=domain,
                                      hostname=hostname,
                                      content=content,
                                      ttl=ttl)

    if result:
        ret['result'] = True
        ret['comment'] = 'Added record to zone {0}'.format(name)
    else:
        ret['comment'] = 'failed to update zone {0}'.format(name)

    return ret

def add_zone(name=None, ns1=None, ns2=None):

    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    result = __salt__['pdns.add_zone'](name=name,
                                      ns1=ns1,
                                      ns2=ns2)

    if result:
        ret['result'] = True
        ret['comment'] = 'added zone {0}'.format(name)
    else:
        ret['comment'] = 'failed to add zone {0}'.format(name)

    return ret

