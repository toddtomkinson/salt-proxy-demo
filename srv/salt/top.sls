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
  'lb.*':
    - lb
    - apps.nginx-lb
    - apps.apache-lb
  'marathon-cluster':
    - apps.hello
    - apps.nginx
    - apps.apache
  'chronos-cluster':
    - jobs.hello
