---
# configuration for staging server

env: test
hostname: openecoe-api-test
app_fqdn: test.openecoe.com
#ansible_ssh_user: ubuntu
#ansible_ssh_private_key_file: "{{ lookup('env', 'PWD') }}/server.pem"
git_branch: develop
app_settings: 'config.TestingConfig'