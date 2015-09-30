# -*- coding: utf-8 -*-
'''
Configure Marathon apps.

.. code-block:: yaml
    my_app:
      marathon_app.config:
        - config:
            cmd: "while [ true ] ; do echo 'Hello Marathon' ; sleep 5 ; done"
            cpus: 0.1
            mem: 10
            instances: 3
'''
import copy
import logging

__proxyenabled__ = ['marathon']
log = logging.getLogger(__file__)


def _compare_configs(config, update_config, changes, namespace=''):
    if isinstance(config, dict):
        if not update_config or not isinstance(update_config, dict):
            changes[namespace] = {
                'new': config,
                'old': update_config,
            }
            return config
        else:
            for key, value in config.iteritems():
                _namespace = key
                if namespace:
                    _namespace = '%s.%s' % (namespace, _namespace)
                _update = None
                if key in update_config:
                    _update = update_config[key]
                update_config[key] = _compare_configs(
                    config[key],
                    _update,
                    changes,
                    namespace=_namespace,
                )
            return update_config
    elif isinstance(config, list):
        #TODO: need to account for empty lists
        if not update_config or not isinstance(update_config, list):
            changes[namespace] = {
                'new': config,
                'old': update_config,
            }
            return config
        else:
            for idx, item in enumerate(config):
                _namespace = '[%s]' % idx
                if namespace:
                    _namespace = '%s%s' % (namespace, _namespace)
                _update = None
                if len(update_config) > idx:
                    _update = update_config[idx]
                if _update:
                    update_config[idx] = _compare_configs(
                        config[idx],
                        _update,
                        changes,
                        namespace=_namespace,
                    )
                else:
                    changes[_namespace] = {
                        'new': config[idx],
                        'old': _update,
                    }
                    update_config.append(config[idx])
            return update_config
    else:
        if config != update_config:
            changes[namespace] = {
                'new': config,
                'old': update_config,
            }
        return config


def config(name, config):
    '''
    Ensure that the marathon app with the given id is present and is configured
    to match the given config values.
    '''
    # setup return structure
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
    }

    # get existing config if app is present
    existing_config = None
    if __salt__['marathon.has_app'](name):
        existing_config = __salt__['marathon.app'](name)['app']

    # compare existing config with defined config
    if existing_config:
        update_config = copy.deepcopy(existing_config)
        _compare_configs(
            config,
            update_config,
            ret['changes'],
        )
    else:
        # the app is not configured--we need to create it from scratch
        ret['changes']['app'] = {
            'new': config,
            'old': None,
        }
        update_config = config

    # update the config if we registered any changes
    if ret['changes']:
        # if test report there will be an update
        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'Marathon app {0} is set to be updated'.format(
                name
            )
            return ret

        update_result = __salt__['marathon.update_app'](name, update_config)
        if 'exception' in update_result:
            ret['result'] = False
            ret['comment'] = 'Failed to update app config for {0}: {1}'.format(
                name,
                update_result['exception'],
            )
            return ret
        else:
            ret['result'] = True
            ret['comment'] = 'Updated app config for {0}'.format(name)
            return ret
    ret['result'] = True
    ret['comment'] = 'Marathon app {0} configured correctly'.format(name)
    return ret


def absent(name):
    '''
    Ensure that the marathon app with the given id is not present.
    '''
    ret = {'name': name,
           'changes': {},
           'result': False,
           'comment': ''}
    if not __salt__['marathon.has_app'](name):
        ret['result'] = True
        ret['comment'] = 'App {0} already absent'.format(name)
        return ret
    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'App {0} is set to be removed'.format(name)
        return ret
    if __salt__['marathon.rm_app'](name):
        ret['changes'] = {'app': name}
        ret['result'] = True
        ret['comment'] = 'Removed app {0}'.format(name)
        return ret
    else:
        ret['result'] = False
        ret['comment'] = 'Failed to remove app {0}'.format(name)
        return ret
