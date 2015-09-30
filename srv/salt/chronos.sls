chronos-packages:
  pkg.latest:
    - name: chronos

chronos-env-file:
  file.managed:
    - name: /etc/sysconfig/chronos
    - contents: |
        LIBPROCESS_PORT="9999"
        LIBPROCESS_IP="{%- set ips = salt['grains.get']('fqdn_ip4', ['127.0.0.1']) -%}{%- if ips[0] != '127.0.0.1' -%}{{ ips[0] }}{%- elif ips|length > 1 and ips[1] != '127.0.0.1' -%}{{ ips[1] }}{%- else -%}{{ ips[0] }}{%- endif -%}"
    - user: root
    - group: root
    - mode: 644
    - template: jinja

chronos-service:
  service.running:
    - name: chronos
    - enable: True
    - watch:
      - pkg: chronos-packages
      - file: chronos-env-file
