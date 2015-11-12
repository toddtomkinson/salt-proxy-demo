##Salt Proxy Minion Demo

This project sets up a local Vagrant salt cluster, including 1 master and 3
minions. The salt configuration sets up a mesos/marathon/chronos cluster on the
3 salt minions, and additionally sets up 2 proxy minions on the master, one to
manage the marathon cluster and another to manage the chronos cluster.

Usage
---
The Vagrantfile assumes that the vagrant-hostmanager plugin is installed. It
can be installed with the following command:

- `vagrant plugin install vagrant-hostmanager`

To initialize the cluster run the following command:

- `vagrant up`

To finish the salt setup login to the master node, accept the pending minion
keys, then perform a highstate:

- `vagrant ssh saltmaster`
- `sudo salt-key -A`
- `sudo salt \* state.highstate` (you may need to run this more than once)

Now accept the proxy minion keys and run a highstate on the marathon and
chronos clusters:

- `sudo salt-key -A`
- `sudo salt \* state.highstate`

The srv/salt and srv/pillar directories in this project are mapped to the
/srv/salt and /srv/pillar directories on the master, meaning that any state or
pillar configuration in this project will be available to the cluster.

The virtual machines will be available to your local host machine with the
following hostnames (the hostmanager plugins adds these to your /etc/hosts
file):

- saltmaster.dev.saltstack.net
- mesos-1.dev.saltstack.net
- mesos-2.dev.saltstack.net
- mesos-3.dev.saltstack.net

