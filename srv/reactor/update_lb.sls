refresh_lb:
  local.state.highstate:
    - tgt: lb.dev.saltstack.net

