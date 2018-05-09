---
# configuration for production

env: production
hostname: openecoe
app_fqdn: openecoe.com
#ansible_ssh_user: ubuntu
#ansible_ssh_private_key_file: "{{ lookup('env', 'PWD') }}/server.pem"
git_repo_setup: true
git_branch: server_deployment