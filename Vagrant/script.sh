#!/bin/sh

apt-get update

apt-get install -y apache2
systemctl start apache2.service
systemctl enable apache2.service

apt-get install -y git
apt-get install -y python3

apt-get install -y mariadb-server-5.5
systemctl start mariadb.service
systemctl enable mariadb.service

git clone http://atlas.umh.es/openECOE/openECOE-API.git

#Falta por eliminar la iteración con el usuario
# Usuario: Segura
# Contraseña: 4314xxzz


