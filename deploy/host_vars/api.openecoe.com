---
# configuration for production

env: production
hostname: openecoe-api
app_fqdn: api.openecoe.com
#ansible_ssh_user: ubuntu
#ansible_ssh_private_key_file: "{{ lookup('env', 'PWD') }}/server.pem"
git_branch: server_deployment
app_settings: 'config.ProductionConfig'