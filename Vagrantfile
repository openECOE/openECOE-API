# -*- mode: ruby -*-
# vi: set ft=ruby :

LOCAL_DOMAIN = "local.openecoe.es"

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/bionic64"
    config.vm.define "develop"
    config.vm.hostname = "openecoe-api-dev"

    config.vm.network "public_network"
    config.vm.synced_folder "./deploy/ansible", "/tmp/deploy", mount_options: ["dmode=775,fmode=664"]

    config.vm.synced_folder ".", "/vagrant", disabled: true
    config.vm.synced_folder ".", "/opt/"+LOCAL_DOMAIN+"/openECOE-API"

    config.vm.network "private_network", ip: "192.168.11.21"

    config.vm.provision "ansible_local" do |ansible|
        #ansible.verbose = "vvv"
        ansible.limit = "api"
        ansible.provisioning_path = "/tmp/deploy"
        ansible.inventory_path = "inventory/develop"
        ansible.playbook = "setup.yml"
        ansible.extra_vars = "@./configurations/template.conf"
    end

    config.vm.define "ubuntu19", autostart: false do |ubuntu19|
        ubuntu19.vm.box = "ubuntu/eoan64"
        ubuntu19.vm.network "private_network", ip: "192.168.111.21"

        #prod.ssh.port = 2232
        #prod.ssh.guest_port = 2252

        ubuntu19.vm.hostname = "openecoe"

        ubuntu19.vm.provision "ansible_local" do |ansible|
          #ansible.verbose = "vvv"
          ansible.limit = "api"
          ansible.provisioning_path = "/tmp/deploy"
          ansible.inventory_path = "inventory/develop"
          ansible.playbook = "setup.yml"
          ansible.extra_vars = "@./configurations/template.conf"
        end
      end


    config.vm.provider "virtualbox" do |v|
        v.memory = 4096
        v.cpus = 2
    end
end