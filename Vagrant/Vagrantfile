
Vagrant.configure("2") do |config|  
  config.vm.box = "ubuntu/trusty64"



 # config.vm.provision “ansible” do |ansible|
 #   ansible.playbook = “instrucciones.yml”
 # end

  config.vm.network "public_network"
  config.vm.provision :shell, :path => "script.sh"
  config.vm.network :forwarded_port, guest: 80, host: 4567
  
  config.ssh.forward_agent = true
  
end