# -*- coding: utf-8 -*-
'''
This module provides a management interface into a chronos cluster.
'''
from __future__ import absolute_import

import json
import logging
import salt.utils.http


__proxyenabled__ = ['chronos']
log = logging.getLogger(__file__)


def __virtual__():
    '''
    '''
    log.debug('chronos proxy __virtual__() called...')
    return 'proxy' in __opts__


def _base_url():
    '''
    '''
    base_url = "http://locahost:4400"
    if 'proxy' in __opts__:
        base_url = __opts__['proxy'].get('base_url', base_url)
    return base_url


def _jobs():
    '''
    '''
    response = salt.utils.http.query(
        "%s/scheduler/jobs" % _base_url(),
        decode_type='json',
        decode=True,
    )
    jobs = {}
    for job in response['dict']:
        jobs[job.pop('name')] = job
    return jobs


def jobs():
    '''
    Get the currently installed jobs.
    '''
    log.debug('chronos proxy jobs() called...')
    job_names = _jobs().keys()
    job_names.sort()
    return {'jobs': job_names}


def has_job(job_name):
    '''
    Return whether the given job_name is currently configured in the chronos
    cluster.
    '''
    return job_name in _jobs()


def job(name):
    '''
    Get the specified job.
    '''
    log.debug('chronos proxy job() called...')
    jobs = _jobs()
    if name in jobs:
        return {'job': jobs[name]}
    return None


def update_job(name, config):
    '''
    Update the specified job with the given config.
    '''
    log.debug('chronos proxy update_job() called...')
    if 'name' not in config:
        config['name'] = name
    data = json.dumps(config)
    try:
        response = salt.utils.http.query(
            "%s/scheduler/iso8601" % _base_url(),
            method='POST',
            data=data,
            header_dict={
                'Content-Type': 'application/json',
            },
        )
        log.debug('update response: %s', response)
        return {'success': True}
    except Exception, ex:
        log.error('unable to update chronos job: %s', ex.message)
        return {
            'exception': {
                'message': ex.message,
            }
        }


def rm_job(name):
    '''
    Remove the specified job.
    '''
    log.debug('chronos proxy rm_job() called...')
    response = salt.utils.http.query(
        "%s/scheduler/job/%s" % (_base_url(), name),
        method='DELETE',
    )
    return True
