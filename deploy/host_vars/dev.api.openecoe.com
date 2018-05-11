---
# configuration for vagrant

env: develop
hostname: openecoe-api-vagrant
base_path: /vagrant
app_fqdn: dev.api.openecoe.com
app_settings: 'config.DevelopmentConfig'