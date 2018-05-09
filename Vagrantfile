# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.hostname = "openECOE-API"
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "public_network"

  config.vm.define "develop" do |dev|
    dev.vm.network "private_network", ip: "192.168.11.11"
    dev.vm.synced_folder ".", "/vagrant/"+ config.vm.hostname

    dev.vm.provision "ansible" do |ansible|
      #ansible.verbose = "v"
      ansible.limit = "vagrant"
      ansible.galaxy_role_file = "deploy/requeriments.yml"
      ansible.inventory_path = "deploy/inventory/vagrant"
      ansible.playbook = "deploy/setup.yml"
    end
  end

  config.vm.define "production", autostart: false do |prod|
    prod.vm.synced_folder ".", "/vagrant", disabled: true
    prod.vm.network "private_network", ip: "192.168.11.12"

    prod.vm.provision "ansible" do |ansible|
      #ansible.verbose = "vvv"
      ansible.limit = "openecoe.com"
      ansible.vault_password_file  = "deploy/ansible_vault.pass"
      #ansible.galaxy_role_file = "deploy/requeriments.yml"
      ansible.playbook = "deploy/setup.yml"
      ansible.inventory_path = "deploy/inventory/production"
    end
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 2
  end
end
