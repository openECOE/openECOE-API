---
# configuration for production

env: production
hostname: openecoe-api
app_fqdn: api.openecoe.com
#ansible_ssh_user: ubuntu
#ansible_ssh_private_key_file: "{{ lookup('env', 'PWD') }}/server.pem"
ansible_connection: local

git_branch: server_deployment

# Enviroment Config
app_secret_key: 'f24b05095b4748a8b9d13df5cdb8d83c'
app_debug: False
api_auth: True

app_workers: 4

supervisor_user: root
supervisor_password: 'kkGFGhiK06BXdEW9gKi4j5VD'

#Deactivate supervisor http server in production
supervisor_inet_http_server_enable: false