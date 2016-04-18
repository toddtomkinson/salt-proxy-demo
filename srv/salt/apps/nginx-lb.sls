/etc/nginx/conf.d/nginx.conf:
  file.managed:
    - source: salt://files/etc/nginx/conf.d/lb.conf.jinja
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
        appname: nginx
        tasks: {{ salt['mine.get']("marathon-cluster", "marathon.tasks").get("marathon-cluster", {}).get("tasks", {}).get("/nginx", []) | json }}
