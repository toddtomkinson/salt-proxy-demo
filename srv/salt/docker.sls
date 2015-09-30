docker-packages:
  pkg.latest:
    - name: docker

docker-service:
  service.running:
    - name: docker
    - enable: True
    - watch:
      - pkg: docker-packages
