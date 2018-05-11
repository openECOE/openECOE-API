---
# configuration for vagrant

env: develop
hostname: openecoe-api-vagrant
base_path: /vagrant
project_path: /vagrant
app_fqdn: dev.api.openecoe.com
app_port: 5000

# Enviroment Config
app_debug: True
bcrypt_log_rounds: 4
api_auth: False