# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
        config.vm.box = "ubuntu/bionic64"
    config.vm.define "develop"
    config.vm.hostname = "openecoe-api-dev"

    config.vm.network "public_network"
    config.vm.synced_folder "./deploy/ansible", "/tmp/deploy", mount_options: ["dmode=775,fmode=664"]

    config.vm.synced_folder ".", "/vagrant", disabled: true
    config.vm.synced_folder ".", "/opt/openECOE-API"

    config.vm.network "private_network", ip: "192.168.11.21"

    config.vm.provision "ansible_local" do |ansible|
        #ansible.verbose = "vvv"
        ansible.limit = "api"
        ansible.provisioning_path = "/tmp/deploy"
        #ansible.galaxy_role_file = "requeriments.yml"
        ansible.inventory_path = "inventory/develop"
        ansible.playbook = "setup.api.yml"
    end


    config.vm.provider "virtualbox" do |v|
        v.memory = 4096
        v.cpus = 2
    end
end