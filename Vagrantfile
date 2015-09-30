# -*- mode: ruby -*-
# vi: set ft=ruby :

DOMAIN = 'dev.saltstack.net'

def get_minion_configs(num_minions)
  minions = []
  for minion_id in 1..num_minions
    minions << {
      :number => minion_id,
      :name => 'mesos-%s' % minion_id,
      :hostname => 'mesos-%s.%s' % [minion_id, DOMAIN],
      :ip => '192.168.235.1%s' % minion_id,
    }
  end
  return minions
end
minion_confs = get_minion_configs(3)

Vagrant.configure(2) do |config|
  config.vm.box = "geerlingguy/centos7"

  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true

  config.vm.define 'saltmaster' do |master|
    master.vm.hostname = 'saltmaster.%s' % DOMAIN
    master.vm.network "private_network", ip: "192.168.235.10"
    master.vm.provider "virtualbox" do |vm|
      vm.memory = 1024
      vm.cpus = 1
    end
    master.vm.provision "shell", inline: <<-SHELL
      wget -O install_salt.sh https://bootstrap.saltstack.com
      sudo sh install_salt.sh -M git 2015.8

      # master
      sudo rm -Rf /srv/salt && sudo ln -s /vagrant/srv/salt /srv/salt
      sudo rm -Rf /srv/pillar && sudo ln -s /vagrant/srv/pillar /srv/pillar
      sudo mkdir -p /etc/salt/master.d
      sudo printf 'file_roots: {base: [/srv/salt]}' > /etc/salt/master.d/file_roots.conf
      sudo printf 'pillar_roots: {base: [/srv/pillar]}' > /etc/salt/master.d/pillar_roots.conf
      sudo mkdir -p /etc/salt/minion.d
      sudo systemctl stop salt-master
      sleep 2
      sudo systemctl start salt-master

      # minion
      sudo mkdir -p /usr/lib/salt
      sudo rm -Rf /usr/lib/salt/proxy && sudo ln -s /vagrant/usr/lib/salt/proxy /usr/lib/salt/proxy
      sudo printf 'master: 192.168.235.10' > /etc/salt/minion.d/master.conf
      sudo printf 'proxy_dirs: [/usr/lib/salt/proxy]' > /etc/salt/minion.d/proxy_dirs.conf
      sudo systemctl stop salt-minion
      sleep 2
      sudo systemctl start salt-minion
    SHELL
  end

  minion_confs.each do |minion_conf|
    config.vm.define minion_conf[:name] do |minion|
      minion.vm.hostname = minion_conf[:hostname]
      minion.vm.network "private_network", ip: minion_conf[:ip]
      minion.vm.provider "virtualbox" do |vm|
        vm.memory = 2048
        vm.cpus = 2
      end
      minion.vm.provision "shell", inline: <<-SHELL
        wget -O install_salt.sh https://bootstrap.saltstack.com
        sudo sh install_salt.sh git 2015.8
        sudo mkdir -p /etc/salt/minion.d
        sudo printf 'master: 192.168.235.10' > /etc/salt/minion.d/master.conf
        sudo systemctl stop salt-minion
        sleep 2
        sudo systemctl start salt-minion
      SHELL
    end
  end

end
