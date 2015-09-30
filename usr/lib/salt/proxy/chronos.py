# -*- coding: utf-8 -*-
'''
This proxy-minion is designed to connect to and manage a Chronos api endpoint.
'''
from __future__ import absolute_import

import logging
import salt.utils.http


__proxyenabled__ = ['chronos']
CONFIG = {}
CONFIG_BASE_URL = 'base_url'
CONFIG_CLUSTER_ID = 'cluster_id'
log = logging.getLogger(__file__)


def __virtual__():
    '''
    Only return if all the modules are available.
    '''
    log.debug('chronos proxy __virtual__() called...')
    return True


def init(opts):
    '''
    Perform any needed setup.
    '''
    log.debug('chronos proxy init() called...')

    if CONFIG_BASE_URL in opts['proxy']:
        CONFIG[CONFIG_BASE_URL] = opts['proxy'][CONFIG_BASE_URL]
    else:
        log.error('missing proxy property %s', CONFIG_BASE_URL)
    if CONFIG_CLUSTER_ID in opts['proxy']:
        CONFIG[CONFIG_CLUSTER_ID] = opts['proxy'][CONFIG_CLUSTER_ID]
    else:
        log.error('missing proxy property %s', CONFIG_CLUSTER_ID)
    log.debug('CONFIG: %s' % CONFIG)


def id(opts):
    '''
    Return the configured cluster_id for this minion.
    '''
    log.debug('chronos proxy id() called...')
    init(opts)
    return CONFIG[CONFIG_CLUSTER_ID]


def ping():
    '''
    Is the chronos api responding?
    '''
    log.debug('chronos proxy ping() called...')
    try:
        response = salt.utils.http.query(
            "%s/scheduler/jobs" % CONFIG[CONFIG_BASE_URL],
            decode_type='json',
            decode=True,
        )
        log.debug(
            'chronos.info returned succesfully: %s',
            response,
        )
        if 'dict' in response:
            return True
    except Exception, ex:
        log.error(
            'error pinging chronos with base_url %s: %s',
            CONFIG[CONFIG_BASE_URL],
            ex,
        )
    return False


def shutdown(opts):
    '''
    For this proxy shutdown is a no-op
    '''
    log.debug('chronos proxy shutdown() called...')
