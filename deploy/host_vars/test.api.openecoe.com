---
# configuration for staging server

env: test
hostname: openecoe-api-test
app_fqdn: test.openecoe.com
ansible_ssh_user: ubuntu
ansible_ssh_private_key_file: "{{ lookup('env', 'PWD') }}/server.pem"

git_branch: develop

# Enviroment Config
app_port: 5000
app_debug: True
app_testing: True
bcrypt_log_rounds: 4
preserve_context_on_exception: False