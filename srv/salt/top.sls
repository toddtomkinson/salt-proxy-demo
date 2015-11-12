base:
  'saltmaster.*':
    - proxies.marathon-cluster
    - proxies.chronos-cluster
  'mesos-*.*':
    - mesosphere_repos
    - zookeeper
    - docker
    - mesos
    - marathon
    - chronos
  'marathon-cluster':
    - apps.hello
    - apps.nginx
  'chronos-cluster':
    - jobs.hello
