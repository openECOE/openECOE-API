# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "public_network"
  config.vm.synced_folder "./deploy", "/tmp/deploy", mount_options: ["dmode=775,fmode=664"]

  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.define "develop" do |dev|
    dev.vm.network "private_network", ip: "192.168.11.11"
    dev.vm.synced_folder ".", "/opt/openECOE-API"

    dev.vm.hostname = "openecoe-api-dev"

    dev.vm.provision "ansible_local" do |ansible|

      #ansible.verbose = "vvv"
      ansible.limit = "develop"
      ansible.provisioning_path = "/tmp/deploy"
      ansible.galaxy_role_file = "requeriments.yml"
      ansible.inventory_path = "inventory/develop"
      ansible.playbook = "setup.yml"

    end
  end

  config.vm.define "production", autostart: false do |prod|
    prod.vm.network "private_network", ip: "192.168.11.12"
    prod.vm.hostname = "openecoe-api"

    prod.vm.provision "ansible_local" do |ansible|
      #ansible.verbose = "vvv"
      ansible.limit = "production"
      ansible.provisioning_path = "/tmp/deploy"
      ansible.vault_password_file  = "ansible_vault.pass"
      ansible.galaxy_role_file = "requeriments.yml"
      ansible.playbook = "setup.yml"
      ansible.inventory_path = "inventory/production"
    end
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 2
  end
end
