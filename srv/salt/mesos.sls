mesos-packages:
  pkg.latest:
    - pkgs:
      - mesos

mesos-zk-config:
  file.managed:
    - name: /etc/mesos/zk
    - source: salt://files/etc/mesos/zk.jinja
    - user: root
    - group: root
    - mode: 644
    - template: jinja

# slave
mesos-slave-work_dir-config:
  file.managed:
    - name: '/etc/mesos-slave/work_dir'
    - contents: "/var/lib/mesos"
    - user: root
    - group: root
    - mode: 644

mesos-slave-ip-config:
  file.managed:
    - name: '/etc/mesos-slave/ip'
    - source: salt://files/ip.jinja
    - user: root
    - group: root
    - mode: 644
    - template: jinja

mesos-slave-containerizers-config:
  file.managed:
    - name: '/etc/mesos-slave/containerizers'
    - contents: "docker,mesos"
    - user: root
    - group: root
    - mode: 644

mesos-slave-executor_registration_timeout-config:
  file.managed:
    - name: '/etc/mesos-slave/executor_registration_timeout'
    - contents: "5mins"
    - user: root
    - group: root
    - mode: 644

mesos-slave-service:
  service.running:
    - name: mesos-slave
    - enable: True
    - reload: True
    - require:
      - file: mesos-slave-work_dir-config
    - watch:
      - file: mesos-zk-config
      - file: '/etc/mesos-slave/*'

# master
mesos-master-quorum-config:
  file.managed:
    - name: '/etc/mesos-master/quorum'
    - contents: '{{ pillar.get('mesos:master:conf:quorum', 2) }}'
    - user: root
    - group: root
    - mode: 644

mesos-master-work_dir-config:
  file.managed:
    - name: '/etc/mesos-master/work_dir'
    - contents: "/var/lib/mesos"
    - user: root
    - group: root
    - mode: 644

mesos-master-ip-config:
  file.managed:
    - name: '/etc/mesos-master/ip'
    - source: salt://files/ip.jinja
    - user: root
    - group: root
    - mode: 644
    - template: jinja

mesos-master-service:
  service.running:
    - name: mesos-master
    - enable: True
    - require:
      - file: mesos-master-quorum-config
      - file: mesos-master-work_dir-config
    - watch:
      - file: mesos-zk-config
      - file: '/etc/mesos-master/*'

