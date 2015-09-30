# -*- coding: utf-8 -*-
'''
This module provides a management interface into a marathon cluster.
'''
from __future__ import absolute_import

import json
import logging
import salt.utils.http


__proxyenabled__ = ['marathon']
log = logging.getLogger(__file__)


def __virtual__():
    '''
    '''
    log.debug('marathon proxy __virtual__() called...')
    return 'proxy' in __opts__


def _base_url(provided_base_url=None):
    '''
    '''
    if provided_base_url:
        return provided_base_url
    base_url = "http://locahost:8080"
    if 'proxy' in __opts__:
        base_url = __opts__['proxy'].get('base_url', base_url)
    return base_url


def _app_id(app_id):
    '''
    Make sure the app_id is in the correct format.
    '''
    if app_id[0] != '/':
        app_id = '/{0}'.format(app_id)
    return app_id


def apps(base_url=None):
    '''
    Get the currently installed apps.
    '''
    log.debug('marathon proxy apps() called...')
    response = salt.utils.http.query(
        "%s/v2/apps" % _base_url(base_url),
        decode_type='json',
        decode=True,
    )
    return {'apps': [app['id'] for app in response['dict']['apps']]}


def has_app(app_id):
    '''
    Return whether the given app_id is currently configured in the marathon
    cluster.
    '''
    return _app_id(app_id) in apps()['apps']


def app(id, base_url=None):
    '''
    Get the specified app.
    '''
    log.debug('marathon proxy app() called...')
    response = salt.utils.http.query(
        "%s/v2/apps/%s" % (_base_url(base_url), id),
        decode_type='json',
        decode=True,
    )
    return response['dict']


def update_app(id, config, base_url=None):
    '''
    Update the specified app with the given config.
    '''
    log.debug('marathon proxy update_app() called...')
    if 'id' not in config:
        config['id'] = id
    config.pop('version', None)
    data = json.dumps(config)
    try:
        response = salt.utils.http.query(
            "%s/v2/apps/%s?force=true" % (_base_url(base_url), id),
            method='PUT',
            decode_type='json',
            decode=True,
            data=data,
            header_dict={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )
        log.debug('update response: %s', response)
        return response['dict']
    except TypeError, ex:
        log.error('unable to update marathon app: %s', ex.message)
        return {
            'exception': {
                'message': ex.message,
            }
        }
    except Exception, ex:
        log.error('unable to update marathon app: (%s) %s', ex.code, ex.message)
        return {
            'exception': {
                'code': ex.code,
                'message': ex.message,
            }
        }


def rm_app(id, base_url=None):
    '''
    Remove the specified app.
    '''
    log.debug('marathon proxy rm_app() called...')
    response = salt.utils.http.query(
        "%s/v2/apps/%s" % (_base_url(base_url), id),
        method='DELETE',
        decode_type='json',
        decode=True,
    )
    return response['dict']


def info(base_url=None):
    '''
    Get info about the marathon instance.
    '''
    log.debug('marathon proxy info() called...')
    response = salt.utils.http.query(
        "%s/v2/info" % _base_url(base_url),
        decode_type='json',
        decode=True,
    )
    return response['dict']
