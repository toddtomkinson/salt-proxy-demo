# -*- coding: utf-8 -*-
'''
Configure Chronos jobs.

.. code-block:: yaml
    my_job:
      chronos_job.config:
        - config:
            schedule: "R//PT2S"
            command: "echo 'hi'"
            owner: "tomkinso@adobe.com"
'''
import copy
import logging

__proxyenabled__ = ['chronos']
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
    Ensure that the chronos job with the given name is present and is configured
    to match the given config values.
    '''
    # setup return structure
    ret = {
        'name': name,
        'changes': {},
        'result': False,
        'comment': '',
    }

    # get existing config if job is present
    existing_config = None
    if __salt__['chronos.has_job'](name):
        existing_config = __salt__['chronos.job'](name)['job']

    # compare existing config with defined config
    if existing_config:
        update_config = copy.deepcopy(existing_config)
        _compare_configs(
            config,
            update_config,
            ret['changes'],
        )
    else:
        # the job is not configured--we need to create it from scratch
        ret['changes']['job'] = {
            'new': config,
            'old': None,
        }
        update_config = config

    if ret['changes']:
        # if the only change is in schedule, check to see if patterns are equivalent
        if 'schedule' in ret['changes'] and len(ret['changes']) == 1:
            if 'new' in ret['changes']['schedule'] and 'old' in ret['changes']['schedule']:
                new = ret['changes']['schedule']['new']
                log.debug('new schedule: %s', new)
                old = ret['changes']['schedule']['old']
                log.debug('old schedule: %s', old)
                if new and old:
                    _new = new.split('/')
                    log.debug('_new schedule: %s', _new)
                    _old = old.split('/')
                    log.debug('_old schedule: %s', _old)
                    if len(_new) == 3 and len(_old) == 3:
                        log.debug('_new[0] == _old[0]: %s', str(_new[0]) == str(_old[0]))
                        log.debug('_new[2] == _old[2]: %s', str(_new[2]) == str(_old[2]))
                        if str(_new[0]) == str(_old[0]) and str(_new[2]) == str(_old[2]):
                            log.debug('schedules match--no need for changes')
                            ret['changes'] = {}

    # update the config if we registered any changes
    log.debug('schedules match--no need for changes')
    if ret['changes']:
        # if test report there will be an update
        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'Chronos job {0} is set to be updated'.format(
                name
            )
            return ret

        update_result = __salt__['chronos.update_job'](name, update_config)
        if 'exception' in update_result:
            ret['result'] = False
            ret['comment'] = 'Failed to update job config for {0}: {1}'.format(
                name,
                update_result['exception'],
            )
            return ret
        else:
            ret['result'] = True
            ret['comment'] = 'Updated job config for {0}'.format(name)
            return ret
    ret['result'] = True
    ret['comment'] = 'Chronos job {0} configured correctly'.format(name)
    return ret


def absent(name):
    '''
    Ensure that the chronos job with the given name is not present.
    '''
    ret = {'name': name,
           'changes': {},
           'result': False,
           'comment': ''}
    if not __salt__['chronos.has_job'](name):
        ret['result'] = True
        ret['comment'] = 'Job {0} already absent'.format(name)
        return ret
    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'Job {0} is set to be removed'.format(name)
        return ret
    if __salt__['chronos.rm_job'](name):
        ret['changes'] = {'job': name}
        ret['result'] = True
        ret['comment'] = 'Removed job {0}'.format(name)
        return ret
    else:
        ret['result'] = False
        ret['comment'] = 'Failed to remove job {0}'.format(name)
        return ret
