# -*- coding: utf-8 -*-
'''
Generate marathon proxy minion grains.
'''
from __future__ import absolute_import


import salt.utils.http
__proxyenabled__ = ['marathon']
__virtualname__ = 'marathon'


def __virtual__():
    if 'proxy' not in __opts__:
        return False
    else:
        return __virtualname__


def kernel():
    return {'kernel': 'marathon'}


def os():
    return {'os': 'marathon'}


def os_family():
    return {'os_family': 'marathon'}


def os_data():
    return {'os_data': 'marathon'}


def marathon():
    response = salt.utils.http.query(
        "%s/v2/info" % __opts__['proxy'].get(
            'base_url',
            "http://locahost:8080",
        ),
        decode_type='json',
        decode=True,
    )
    return {'marathon': response['dict']}