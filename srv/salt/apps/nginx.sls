nginx:
  marathon_app.config:
    - config:
        cpus: 0.5
        mem: 128
        instances: 3
        container:
          type: DOCKER
          docker:
            network: BRIDGE
            image: nginx:latest
            portMappings:
              - containerPort: 80
                hostPort: 0
