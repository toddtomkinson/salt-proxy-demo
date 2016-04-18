/etc/nginx/conf.d/apache.conf:
  file.managed:
    - source: salt://files/etc/nginx/conf.d/lb.conf.jinja
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
        appname: apache
        tasks: {{ salt['mine.get']("marathon-cluster", "marathon.tasks").get("marathon-cluster", {}).get("tasks", {}).get("/apache", []) | json }}
