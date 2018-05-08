# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  project_name = "openECOE-API"

  config.vm.hostname = project_name
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "public_network"
  config.vm.network "private_network", ip: "192.168.11.11"

  config.vm.define "develop" do |dev|
    dev.vm.network "forwarded_port", guest: 5000, host: 5000
    dev.vm.synced_folder ".", "/vagrant/"+ project_name

    dev.vm.provision "ansible" do |ansible|
      #ansible.verbose = "v"
      ansible.limit = "vagrant"
      #ansible.galaxy_role_file = "deploy/requeriments.yml"
      ansible.inventory_path = "deploy/inventory/vagrant"
      ansible.playbook = "deploy/setup.yml"
    end
  end

  config.vm.define "production", autostart: false do |prod|
    prod.vm.synced_folder ".", "/vagrant", disabled: true

    prod.vm.provision "ansible" do |ansible|
      ansible.limit = "openecoe.com"
      #ansible.ask_vault_pass = true
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
