marathon-packages:
  pkg.latest:
    - name: marathon

marathon-env-file:
  file.managed:
    - name: /etc/sysconfig/marathon
    - contents: |
        LIBPROCESS_PORT="5555"
        LIBPROCESS_IP="{{ salt['grains.get']('fqdn_ip4', ['127.0.0.1'])|first() }}"
    - user: root
    - group: root
    - mode: 644
    - template: jinja

marathon-service:
  service.running:
    - name: marathon
    - enable: True
    - reload: True
    - watch:
      - pkg: marathon-packages
      - file: marathon-env-file
