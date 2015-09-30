marathon-packages:
  pkg.latest:
    - name: marathon

marathon-env-file:
  file.managed:
    - name: /etc/sysconfig/marathon
    - contents: |
        LIBPROCESS_PORT="5555"
        LIBPROCESS_IP="{%- set ips = salt['grains.get']('fqdn_ip4', ['127.0.0.1']) -%}{%- if ips[0] != '127.0.0.1' -%}{{ ips[0] }}{%- elif ips|length > 1 and ips[1] != '127.0.0.1' -%}{{ ips[1] }}{%- else -%}{{ ips[0] }}{%- endif -%}"
    - user: root
    - group: root
    - mode: 644
    - template: jinja

marathon-service:
  service.running:
    - name: marathon
    - enable: True
    - watch:
      - pkg: marathon-packages
      - file: marathon-env-file
