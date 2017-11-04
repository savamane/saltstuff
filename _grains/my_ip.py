# -*- coding: utf-8 -*-
'''
    :codeauthor: sava
    :license: BSD

    salt.grains.my_ip
    ~~~~~~~~~~~~~~~~~~~~~~~

    Returns the first IPv4 from `hostname -I`

'''

import commands

def my_ip():
    '''
    Return first entry of `hostname -I`
    '''

    IPv4 = commands.getoutput('hostname -I').split(" ")[0]
    return { 'my_ip': IPv4 }
