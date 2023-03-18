#!/bin/bash
cd /app/api
if flask virgin;
then
flask create_orga --name $ORGANIZATION;
flask create_user --email $EMAIL --password $PASSWORD --name $FIRSTNAME --surname $SURNAME --organization_name $ORGANIZATION --admin;
fi;
