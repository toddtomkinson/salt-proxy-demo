zookeeper:
  servers:
    1:
      host: mesos-1.dev.saltstack.net
      leader_port: 2888
      election_port: 3888
    2:
      host: mesos-2.dev.saltstack.net
      leader_port: 2888
      election_port: 3888
    3:
      host: mesos-3.dev.saltstack.net
      leader_port: 2888
      election_port: 3888

mesos:
  master:
    conf:
      quorum: 2

