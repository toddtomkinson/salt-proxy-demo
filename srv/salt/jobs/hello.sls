hello:
  #  chronos_job.absent: []
  chronos_job.config:
    - config:
        schedule: "R//PT2S"
        command: "echo 'hi'"
        owner: "tomkinso@adobe.com"

