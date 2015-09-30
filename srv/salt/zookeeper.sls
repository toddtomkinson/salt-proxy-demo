include:
  - mesosphere_repos

zookeeper-packages:
  pkg.latest:
    - pkgs:
      - mesosphere-zookeeper

zookeeper-user:
  group.present:
    - name: zookeeper
  user.present:
    - name: zookeeper
    - fullname: ZooKeeper
    - shell: /sbin/nologin
    - home: /data/zookeeper
    - createhome: False
    - gid_from_name: True

zookeeper-datadir:
  file.directory:
    - name: /data/zookeeper
    - makedirs: True
    - user: zookeeper
    - group: zookeeper
    - mode: 755
    - require:
      - user: zookeeper-user
      - group: zookeeper-user

zookeeper-log_directory:
  file.directory:
    - name: /var/log/zookeeper
    - makedirs: True
    - user: zookeeper
    - group: zookeeper
    - mode: 755
    - require:
      - user: zookeeper-user
      - group: zookeeper-user

zookeeper-config_file:
  file.managed:
    - name: /etc/zookeeper/conf/zoo.cfg
    - source: salt://files/etc/zookeeper/conf/zoo.cfg.jinja
    - user: root
    - group: root
    - mode: 644
    - template: jinja

zookeeper-myid_file:
  file.managed:
    - name: /data/zookeeper/myid
    - source: salt://files/myid.jinja
    - user: zookeeper
    - group: zookeeper
    - mode: 644
    - template: jinja
    - require:
      - user: zookeeper-user
      - group: zookeeper-user

zookeeper-log4j_properties:
  file.managed:
    - name: /etc/zookeeper/conf/log4j.properties
    - source: salt://files/etc/zookeeper/conf/log4j.properties
    - user: root
    - group: root
    - mode: 644

zookeeper-service_definition:
  file.managed:
    - name: /usr/lib/systemd/system/zookeeper.service
    - source: salt://files/usr/lib/systemd/system/zookeeper.service
    - user: root
    - group: root
    - mode: 644

zookeeper-service:
  service.running:
    - name: zookeeper
    - enable: True
    - reload: True
    - require:
      - file: zookeeper-log_directory
      - file: zookeeper-datadir
    - watch:
      - pkg: zookeeper-packages
      - file: zookeeper-service_definition
      - file: zookeeper-config_file
      - file: zookeeper-log4j_properties
      - file: zookeeper-myid_file
