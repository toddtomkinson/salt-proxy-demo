# -*- coding: utf-8 -*-
'''
Marathon
========

Proxy minion for managing a Marathon cluster.

Dependencies
------------

- :doc:`marathon execution module (salt.modules.marathon) </ref/modules/all/salt.modules.marathon>`

Pillar
------

The marathon proxy configuration requires a 'base_url' property that points to
the marathon endpoint:

.. code-block:: yaml

    proxy:
      proxytype: marathon
      base_url: http://my-marathon-master.mydomain.com:8080

.. versionadded:: 2015.8.2
'''
from __future__ import absolute_import

import logging
import threading

import salt.utils.http


__proxyenabled__ = ['marathon']
CONFIG = {}
CONFIG_BASE_URL = 'base_url'
DETAILS = {}
log = logging.getLogger(__file__)


try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def __virtual__():
    return True


class EventReceiver(object):
    '''
    Class used to encapsulate a thread that monitors the marathon event stream
    to publish deployment events to other minions.
    '''

    def __init__(self, base_url, minion_id):
        self.running = False
        self.base_url = base_url
        self.minion_id = minion_id

    def start(self):
        '''
        Start the thread that monitors the event stream.
        '''
        self.running = True
        threading.Thread(
            target=self.run,
        ).start()

    def stop(self):
        '''
        Stop the thread that monitors the event stream.
        '''
        self.running = False

    def run(self):
        '''
        The thread's target method that does the work of connecting to the
        event stream, monitoring the stream for deployment_success messages,
        and publishing events to the salt reactor to notify other minions.
        '''
        log.debug("Starting marathon event receiver")
        while True:
            if not self.running:
                break
            try:
                log.debug("Making marathon event receiver request")
                response = requests.get(
                    "{0}/v2/events".format(self.base_url),
                    stream=True,
                    headers={
                        'Accept': 'text/event-stream',
                        'Cache-Control': 'no-cache',
                    },
                )
                for line in response.iter_lines():
                    log.debug("Marathon event stream line: %s", line)
                    # we only care about deployment_success events (for now)
                    if 'event: deployment_success' in line:
                        log.info('Marathon event: deployment_success')
                        # update the registered mine functions
                        __salt__['mine.update']()
                        # publish the deployment_success event
                        __salt__['event.send'](
                            'salt/marathon/{0}/deployment_success'.format(
                                self.minion_id
                            )
                        )
            except Exception as ex:
                log.error(
                    'error calling marathon event stream with base_url %s: %s',
                    CONFIG[CONFIG_BASE_URL],
                    ex,
                )


def init(opts):
    '''
    Perform any needed setup.
    '''
    if CONFIG_BASE_URL in opts['proxy']:
        CONFIG[CONFIG_BASE_URL] = opts['proxy'][CONFIG_BASE_URL]
    else:
        log.error('missing proxy property %s', CONFIG_BASE_URL)
    log.debug('CONFIG: %s', CONFIG)

    if HAS_REQUESTS:
        # start a background thread that monitors the marathon server side
        # event stream and listens for new deployments
        DETAILS['er'] = EventReceiver(CONFIG[CONFIG_BASE_URL], opts['id'])
        DETAILS['er'].start()


def ping():
    '''
    Is the marathon api responding?
    '''
    try:
        response = salt.utils.http.query(
            "{0}/ping".format(CONFIG[CONFIG_BASE_URL]),
            decode_type='plain',
            decode=True,
        )
        log.debug(
            'marathon.info returned succesfully: %s',
            response,
        )
        if 'text' in response and response['text'].strip() == 'pong':
            return True
    except Exception as ex:
        log.error(
            'error calling marathon.info with base_url %s: %s',
            CONFIG[CONFIG_BASE_URL],
            ex,
        )
    return False


def shutdown(opts):
    '''
    Cleanup any resources used by the proxy minion.
    '''
    log.debug('marathon proxy shutdown() called...')
    if HAS_REQUESTS:
        # stop the background thread
        DETAILS['er'].stop()
