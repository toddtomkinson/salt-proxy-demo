apache:
  marathon_app.config:
    - config:
        cpus: 0.25
        mem: 128
        instances: 3
        container:
          type: DOCKER
          docker:
            network: BRIDGE
            image: httpd:latest
            portMappings:
              - containerPort: 80
                hostPort: 0
