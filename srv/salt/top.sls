base:
  'saltmaster.*':
    - proxies.marathon-cluster
  'mesos-*.*':
    - mesosphere_repos
    - zookeeper
    - docker
    - mesos
    - marathon
  'marathon-cluster':
    - apps.hello
