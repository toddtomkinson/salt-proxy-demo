base:
  'saltmaster.*': []
  'mesos-*.*':
    - mesos
  'marathon-cluster':
    - marathon-cluster
  'chronos-cluster':
    - chronos-cluster
