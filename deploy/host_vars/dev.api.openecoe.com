---
# configuration for vagrant

env: develop
hostname: openecoe-api-vagrant
app_fqdn: dev.api.openecoe.com
app_port: 5000

#ansible_ssh_user: ubuntu
#ansible_ssh_private_key_file: "{{ lookup('env', 'PWD') }}/server.pem"
ansible_connection: local

# Enviroment Config
app_debug: True
bcrypt_log_rounds: 4
api_auth: False