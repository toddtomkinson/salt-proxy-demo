/etc/salt/proxies/marathon-cluster:
  file.directory:
    - user: root
    - group: root
    - mode: 755
    - makedirs: True

/etc/salt/proxies/marathon-cluster/proxy:
  file.managed:
    - contents: |
        master: saltmaster.dev.saltstack.net
        proxy_dirs: [/usr/lib/salt/proxy]
        root_dir: /etc/salt/proxies/marathon-cluster
        add_proxymodule_to_opts: False
    - user: root
    - group: root
    - mode: 644

/usr/lib/systemd/system/marathon-cluster-minion.service:
  file.managed:
    - source: salt://files/usr/lib/systemd/system/proxy-minion.service.jinja
    - defaults:
        minion_id: marathon-cluster
        minion_dir: /etc/salt/proxies/marathon-cluster
    - user: root
    - group: root
    - mode: 644
    - template: jinja

marathon-cluster-minion:
  service.running:
    - enable: True
    - require:
      - file: /usr/lib/systemd/system/marathon-cluster-minion.service
    - watch:
      - file: /usr/lib/systemd/system/marathon-cluster-minion.service

