nginx-packages:
  pkg.latest:
    - name: nginx

/etc/nginx/conf.d/default.conf:
  file.absent: []

nginx-service:
  service.running:
    - name: nginx
    - enable: True
    - watch:
      - pkg: nginx-packages
      - file: /etc/nginx/conf.d/*
