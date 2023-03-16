#!/bin/bash
cd /app/api
if ./env/bin/flask virgin;
then
./env/bin/flask create_orga --name $ORGANIZATION;
./env/bin/flask create_user --email $EMAIL --password $PASSWORD --name $FIRSTNAME --surname $SURNAME --organization_name $ORGANIZATION --admin;
fi;
