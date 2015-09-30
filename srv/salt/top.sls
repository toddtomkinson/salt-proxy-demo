base:
  'saltmaster.*': []
  'mesos-*.*':
    - mesosphere_repos
    - zookeeper
    - docker
    - mesos
    - marathon
  'marathon-cluster':
    - apps.hello
