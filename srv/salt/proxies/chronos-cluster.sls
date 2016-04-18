/etc/salt/proxies/chronos-cluster:
  file.directory:
    - user: root
    - group: root
    - mode: 755
    - makedirs: True

/etc/salt/proxies/chronos-cluster/proxy:
  file.managed:
    - contents: |
        master: saltmaster.dev.saltstack.net
        proxy_dirs: [/usr/lib/salt/proxy]
        root_dir: /etc/salt/proxies/chronos-cluster
        add_proxymodule_to_opts: False
    - user: root
    - group: root
    - mode: 644
    - require:
      - file: /etc/salt/proxies/marathon-cluster

/usr/lib/systemd/system/chronos-cluster-minion.service:
  file.managed:
    - source: salt://files/usr/lib/systemd/system/proxy-minion.service.jinja
    - defaults:
        minion_id: chronos-cluster
        minion_dir: /etc/salt/proxies/chronos-cluster
    - user: root
    - group: root
    - mode: 644
    - template: jinja

chronos-cluster-minion:
  service.running:
    - enable: True
    - require:
      - file: /usr/lib/systemd/system/chronos-cluster-minion.service
      - file: /etc/salt/proxies/marathon-cluster/proxy
    - watch:
      - file: /usr/lib/systemd/system/chronos-cluster-minion.service
      - file: /etc/salt/proxies/marathon-cluster/proxy

